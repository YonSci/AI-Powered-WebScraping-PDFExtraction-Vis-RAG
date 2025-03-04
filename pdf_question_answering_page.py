import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import streamlit as st

from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering, T5Tokenizer, T5ForConditionalGeneration
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import tempfile
import logging
import nltk
from typing import List, Optional

# Download the punkt tokenizer models
nltk.download('punkt')

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    langchain_available = True
except ImportError:
    logging.warning("LangChain is not installed. Semantic Chunking with Langchain will be unavailable.")
    langchain_available = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize session state variables at the top level
if 'vector_store' not in st.session_state:
    st.session_state['vector_store'] = {}  # {chunk_id: embedding}
if 'document_chunks' not in st.session_state:
    st.session_state['document_chunks'] = {}  # {chunk_id: chunk_text}
if 'chunk_metadata' not in st.session_state:
    st.session_state['chunk_metadata'] = {}  # {chunk_id: {file_name:..., start:..., end:...}}
if 'selected_chunking_strategy' not in st.session_state:
    st.session_state['selected_chunking_strategy'] = "Fixed Size with Overlap"
if 'chunk_size' not in st.session_state:
    st.session_state['chunk_size'] = 1000
if 'overlap' not in st.session_state:
    st.session_state['overlap'] = 200
if 'question' not in st.session_state:
    st.session_state['question'] = ""
if 'selected_embedding_model_name' not in st.session_state:
    st.session_state['selected_embedding_model_name'] = 'all-mpnet-base-v2'  # Default model
if 'selected_qa_model' not in st.session_state:
    st.session_state['selected_qa_model'] = 'DistilBERT (default)'

def pdf_question_answering_page():
    st.markdown(
    """
    <div style='background-color: #e0f2f7; padding: 20px; border-radius: 10px;'>
        <h1 style='text-align: center; color: #007BFF;'>📄 RAG Dashboard: Chat with Uploaded PDF Documents</h1>
    </div>
    """,
    unsafe_allow_html=True,
    )
    st.markdown("""
    **How it works:**

    1. 📤 Upload PDF files.
    2. ✍️ Type your question in plain English.
    3. 🧩 The system extracts text, splits it into chunks, and finds the most relevant ones.
    4. 🤖 A QA engine answers based on the context.
    5. 📑 Relevant document snippets are shown.
    """)

    st.markdown("---")

    # --------------------------
    # Document Loading and Parsing
    # --------------------------
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(file_bytes)
            full_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            return full_text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}. Please ensure the PDF is not corrupted.")
            logging.error(f"Error extracting text from PDF: {e}", exc_info=True)  # Log the full traceback
            return ""

    def load_document(file: bytes, file_name: str) -> Optional[str]:
        if file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        else:
            st.error(f"Unsupported file type for {file_name}")
            return None

        if not text.strip():
            st.error(f"No text could be extracted from {file_name}. Please check the file content.")
            return None
        return text

    # --------------------------
    # Chunking Strategy
    # --------------------------
    def chunk_text_fixed_overlap(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Fixed-size chunking with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def chunk_text_fixed_no_overlap(text: str, chunk_size: int = 1000) -> List[str]:
        """Fixed-size chunking without overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end
        return chunks

    def chunk_text_semantic_langchain(text: str) -> List[str]:
        """Semantic chunking using LangChain."""
        if not langchain_available:
            st.error("Semantic chunking with LangChain requires the 'langchain' library. Please install it to use this feature.")
            return []
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_text(text)
            return chunks
        except Exception as e:
            st.error(f"Error during semantic chunking with LangChain: {e}")
            logging.error(f"Error during semantic chunking with LangChain: {e}", exc_info=True)
            return []

    # --------------------------
    # Embedding Generation: Sentence Transformers
    # --------------------------
    # Define the available sentence transformer models
    embedding_model_options = [
        "all-mpnet-base-v2",
        "multi-qa-mpnet-base-dot-v1",
        "msmarco-bert-base-dot-v5",
        "all-MiniLM-L6-v2",
        "sentence-t5-base",
        "msmarco-bert-base-dot-v5",
        "quora-distilbert-multilingual",
        "multi-qa-MiniLM-L6-cos-v1",
        "paraphrase-albert-small-v2",
    ]

    @st.cache_resource(show_spinner=False)
    def load_embedding_model(model_name: str) -> SentenceTransformer:
        return SentenceTransformer(model_name)

    def get_embeddings(text: str, embedding_model: SentenceTransformer) -> Optional[List[float]]:
        try:
            return embedding_model.encode(text, convert_to_tensor=False)
        except Exception as e:
            st.error(f"Error generating embeddings: {e}. Please try again.")
            logging.error(f"Error generating embeddings: {e}", exc_info=True) #Log full traceback
            return None  # Handle embedding failure gracefully

    # --------------------------
    # Vector Store and Embeddings
    # --------------------------
    def store_embeddings(chunks: List[str], file_name: str, embedding_model: SentenceTransformer) -> None:
        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_name}_chunk_{i}"
            embedding = get_embeddings(chunk, embedding_model) # embedding model is used
            if embedding is not None: # Only store valid embeddings
                st.session_state['vector_store'][chunk_id] = embedding
                st.session_state['document_chunks'][chunk_id] = chunk
                st.session_state['chunk_metadata'][chunk_id] = {
                    "file_name": file_name,
                    "start": i * (1000 - 200),
                    "end": (i + 1) * (1000 - 200) + 200,
                }
            else:
                logging.warning(f"Skipping chunk {i} from {file_name} due to embedding failure.")

    def retrieve_relevant_chunks(query_embedding: List[float], top_k: int = 5) -> List[str]:
        similarities = {}
        for chunk_id, chunk_embedding in st.session_state['vector_store'].items():
            try:
                similarity = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
                similarities[chunk_id] = similarity
            except Exception as e:
                logging.error(f"Error calculating cosine similarity for chunk {chunk_id}: {e}", exc_info=True)
                similarities[chunk_id] = -1  # Assign a low similarity score to avoid errors

        sorted_chunks = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        top_chunks = [chunk_id for chunk_id, _ in sorted_chunks[:top_k]]
        return top_chunks

    # --------------------------
    # Generation Component: LLMs
    # --------------------------
    @st.cache_resource(show_spinner=False)
    def load_qa_pipeline(model_name: str):
        try:
            if "t5" in model_name:
                model = T5ForConditionalGeneration.from_pretrained(model_name)
                tokenizer = T5Tokenizer.from_pretrained(model_name)
                return pipeline("text2text-generation", model=model, tokenizer=tokenizer)
            else:
                model = AutoModelForQuestionAnswering.from_pretrained(model_name)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                return pipeline("question-answering", model=model, tokenizer=tokenizer)
        except Exception as e:
            st.error(f"Error loading QA pipeline: {e}. Please check the selected model.")
            logging.error(f"Error loading QA pipeline: {e}", exc_info=True)
            return None  #Handle pipeline failure

    qa_models = {
        "DistilBERT (default)": "distilbert-base-cased-distilled-squad",
        "RoBERTa Base": "deepset/roberta-base-squad2",
        "ALBERT": "Palak/albert-base-v2_squad",
        "MiniLM": "deepset/minilm-uncased-squad2",
        "BERT Large": "bert-large-uncased-whole-word-masking-finetuned-squad",
    }
    # -----------------------------
    # Clear inputs function
    # -----------------------------
    def clear_all_inputs():
        st.session_state['vector_store'] = {}
        st.session_state['document_chunks'] = {}
        st.session_state['chunk_metadata'] = {}
        st.session_state['question'] = ""

    # --------------------------
    # Sidebar Controls
    # --------------------------
    with st.sidebar:
        st.header("⚙️ Controls")
        if st.button("🔄 Clear All Fields", type="primary", help="Clear all the input fields and selections", key="clear_all_button_sidebar"):
            clear_all_inputs()
            st.rerun()

    # --------------------------
    # Layout: File Uploads and Question Input
    # --------------------------
    st.markdown("### 📤 File Uploads and Question Input")
    uploaded_files = st.file_uploader("📤 Upload PDF files", type=["pdf"],
                                      accept_multiple_files=True, key="file_uploader")
    
    question = st.text_area("✍️ Enter your question:", key="question_input")

    st.markdown("---")

    # --------------------------
    # Chunking strategy selection in the main page
    # --------------------------
    st.markdown("### 🧩 Chunking Strategy Selection")
    chunking_strategies = {
        "Fixed Size with Overlap": chunk_text_fixed_overlap,
        "Fixed Size without Overlap": chunk_text_fixed_no_overlap,
    }

    if langchain_available:
        chunking_strategies["Semantic Chunking (LangChain)"] = chunk_text_semantic_langchain

    selected_chunking_strategy = st.selectbox("🧩 Select Chunking Strategy", list(chunking_strategies.keys()), key="chunking_strategy")

    if selected_chunking_strategy in ["Fixed Size with Overlap", "Fixed Size without Overlap"]:
        chunk_size = st.slider("Chunk Size", min_value=100, max_value=2000, value=st.session_state.get('chunk_size', 1000), step=100, key="chunk_size_slider")
        st.session_state['chunk_size'] = chunk_size  # Update session state

        if selected_chunking_strategy == "Fixed Size with Overlap":
            overlap = st.slider("Overlap", min_value=0, max_value=500, value=st.session_state.get('overlap', 200), step=50, key="overlap_slider")
            st.session_state['overlap'] = overlap #update session state
        else:
            overlap = 0
    else:
        chunk_size = 0
        overlap = 0

    # -------------------------
    # Select Sentence Transformer Model
    # -------------------------
    st.markdown("### 🔍 Select Sentence Embedding Model")
    # Ensure the session state is set before the widget is created
    if 'selected_embedding_model_name' not in st.session_state:
        st.session_state['selected_embedding_model_name'] = 'all-mpnet-base-v2'  # Default model

    selected_embedding_model_name = st.selectbox(
        "🔍 Select Sentence Transformer Model",
        embedding_model_options,
        index=embedding_model_options.index(st.session_state['selected_embedding_model_name']), # Default model
        key = "embedding_model_selectbox"
    )

    # -------------------------
    # Select LLM Model
    # -------------------------
    st.markdown("### 🤖 Select Large Language Model (LLM)")
    selected_model = st.selectbox("🤖 Select a Large Language Model (LLM)", list(qa_models.keys()), index=0, key="qa_model_selectbox")
    model_name = qa_models[selected_model]
    qa_pipeline = load_qa_pipeline(model_name)

    max_answer_len = st.slider("Maximum answer length", min_value=5, max_value=50, value=30, key="max_answer_len_slider")
    min_score_threshold = st.slider("Minimum confidence threshold", min_value=0.0, max_value=1.0, value=0.2,
                                    step=0.01, key="min_score_threshold_slider")

    # Load the selected embedding model
    embedding_model = load_embedding_model(selected_embedding_model_name)
    # Processing files
    st.markdown("### 📄 Processing Files")
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False,
                                                      suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_file_path = temp_file.name

                    try:
                        with open(temp_file_path, "rb") as f:
                            full_text = load_document(f, uploaded_file.name)
                            if full_text is None:
                                continue
                            st.success(f"File: {uploaded_file.name} extracted successfully!")

                            # Use the selected chunking strategy
                            selected_strategy_func = chunking_strategies[selected_chunking_strategy]

                            if selected_chunking_strategy == "Fixed Size with Overlap":
                                chunks = selected_strategy_func(full_text, chunk_size, overlap)
                            elif selected_chunking_strategy == "Fixed Size without Overlap":
                                chunks = selected_strategy_func(full_text, chunk_size)
                            else:
                                chunks = selected_strategy_func(full_text)

                            with st.spinner("Generating embeddings..."):
                                store_embeddings(chunks, uploaded_file.name, embedding_model) #add the embedding_model
                    except Exception as e:
                        st.error(f"Error processing file {uploaded_file.name}: {e}")
                        logging.error(f"Error processing file {uploaded_file.name}: {e}", exc_info=True)
                    finally:
                        try:
                            if os.path.exists(temp_file_path):
                                os.remove(temp_file_path)
                        except Exception as e:
                            logging.error(f"Error removing file {temp_file_path}: {e}", exc_info=True)
                except Exception as e:
                    st.error(f"Error creating temporal file  {uploaded_file.name}: {e}")
                    logging.error(f"Error creating temporal file {uploaded_file.name}: {e}", exc_info=True)
        st.markdown("---")
    else:
        st.info("Please upload a PDF file to start.")

    # generate response button
    st.markdown("### 📝 Generate Response")
    if st.button("Generate Response", key="generate_response_button"):
        # ---------------------
        # Processing & QA
        # ---------------------
        if question and st.session_state['vector_store'] and qa_pipeline:  # Check if qa_pipeline is loaded
            query_embedding = get_embeddings(question, embedding_model)
            if query_embedding is not None:  # Ensure query embedding is valid
                relevant_chunk_ids = retrieve_relevant_chunks(query_embedding)

                context = ""
                highlighted_text = ""
                for chunk_id in relevant_chunk_ids:
                    context += st.session_state['document_chunks'][chunk_id] + " "

                with st.spinner("Generating answer..."):
                    try:
                        result = qa_pipeline(
                            question=question,
                            context=context,
                            max_answer_len=max_answer_len
                        )
                        answer = result['answer']
                        score = result['score']
                    except Exception as e:
                        st.error(f"Error running the QA engine: {e}")
                        logging.error(f"Error running the QA engine: {e}", exc_info=True)
                        return

                if score < min_score_threshold:
                    st.warning(
                        "The model's confidence is low. Consider rephrasing your question or checking the document.")
                else:
                    st.subheader("Answer")
                    st.markdown(f"<div style='background-color: #f0f0f5; padding: 10px; border-radius: 5px;'><strong>{answer}</strong></div>", unsafe_allow_html=True)

                    # Enhanced context highlighting.
                    pos = context.lower().find(answer.lower())
                    if pos != -1:
                        start = max(0, pos - 100)
                        end = pos + len(answer) + 100
                        snippet = context[start:end]
                        # Highlight the answer using HTML mark tag.
                        highlighted = snippet.replace(answer, f"<mark>{answer}</mark>")
                        st.subheader("Context Highlight")
                        st.markdown(f"<div style='background-color: #f0f0f5; padding: 10px; border-radius: 5px;'>{highlighted}</div>", unsafe_allow_html=True)
                    else:
                        st.info("Could not determine a context snippet for the answer.")
            else:
                st.error("Failed to generate query embedding.  Please check your document and question.")

        elif not qa_pipeline:
            st.error("QA Pipeline failed to load. Please check the selected model.")
        elif not st.session_state['vector_store']:
            st.warning("No document has been processed yet.")
        elif not question:
            st.warning("Please enter a question.")

pdf_question_answering_page()