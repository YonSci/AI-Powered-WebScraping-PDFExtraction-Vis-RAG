import streamlit as st
from typing import List, Dict, Any


def about_page() -> None:
    """
    Displays the documentation/about page for the AI-Powered Data Analysis Tool.
    """

    st.markdown(
        """
        <div style='background-color: #e0f2f7; padding: 20px; border-radius: 10px;'>
            <h1 style='text-align: center; color: #007BFF;'>📖 Documentation</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")  # Section separator

    st.markdown(
        """
        <h2 style='color: #2196F3;'>🌐 About Synapse Insights</h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
            <p>
                <b>Synapse Insights</b> is an <b>AI-powered</b> data hub designed to extract, analyze, and visualize data from multiple sources.
                It empowers users to transform raw data into actionable insights using a range of cutting-edge techniques.
                Developed in collaboration with the <b>African Centre for Statistics</b> of the <b>Economic Commission for Africa</b>,
                this tool is tailored to the needs of statistical offices and development stakeholders across Africa.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")  # Section separator

    st.markdown(
        """
        <h2 style='color: #2196F3;'>💡 Key Features</h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
            <p>
             Here are the core functionalities of Synapse Insights:
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .feature-item {
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            background-color: #f8f9fa;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='feature-item'>
        <h3>🏠 Home</h3>
        <p>
            The landing page introduces the application's core capabilities and provides a quick start guide.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='feature-item'>
            <h3>🌐 Web Scraping</h3>
            <p>
                Extract <b>structured</b> data and downloadable file links from <b>any website</b>.
                <ul>
                    <li>✅ Support for diverse websites and custom URLs.</li>
                    <li>✅ Advanced filtering based on keywords, years, and months.</li>
                    <li>✅ Pagination handling for multi-page websites.</li>
                    <li>✅ Save and load configurations for recurring tasks.</li>
                    <li>✅ Download extracted files as a ZIP archive.</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='feature-item'>
            <h3>📄 PDF Table Extraction</h3>
            <p>
                Extract <b>structured tabular data</b> from <b>PDF</b> files.
                <ul>
                    <li>✅ Choice between two robust extraction engines: <b>Camelot</b> and <b>Tabula-py</b>.</li>
                    <li>✅ Selection of appropriate extraction method (<b>lattice</b> or <b>stream</b>).</li>
                    <li>✅ Process specific or all pages within a PDF.</li>
                    <li>✅ Interactive table editing for corrections and adjustments.</li>
                    <li>✅ Export to various formats: CSV, Excel, and JSON.</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='feature-item'>
            <h3>📊 Data Visualization</h3>
            <p>
                Explore and visualize your data interactively by uploading <b>CSV or Excel</b> files.
                <ul>
                    <li>✅ Comprehensive data summaries.</li>
                    <li>✅ Option to view the full dataset.</li>
                    <li>✅ Column data type adjustment.</li>
                    <li>✅ Data transformation capabilities.</li>
                    <li>✅ Variety of plot types.</li>
                    <li>✅ Customizable chart properties.</li>
                    <li>✅ download transformed data in CSV format.</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='feature-item'>
            <h3>🤖 RAG-Powered PDF Insights</h3>
            <p>
                Engage in natural language <b>question-answering</b> with your PDF documents.
                <ul>
                    <li>✅ Multiple chunking strategies.</li>
                    <li>✅ Configurable chunk size and overlap.</li>
                    <li>✅ Choice of sentence embedding models.</li>
                    <li>✅ Selection of Large Language Models (LLMs).</li>
                    <li>✅ Display of generated answers with supporting context.</li>
                    <li>✅ Adjustable maximum answer length and minimum confidence threshold.</li>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")  # Section separator

    st.markdown(
        """
        <h2 style='color: #2196F3;'>📖 How to Use</h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
            <p>
             Here are the core steps to use Synapse Insights:
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .use-item {
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            background-color: #f8f9fa;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='use-item'>
        <h3>🏠 Home</h3>
        <p>
            ➡️ Get an overview of Synapse Insights and its core features.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='use-item'>
        <h3>🌐 Web Scraping</h3>
        <p>
            1. ➡️ Select a country or enter a custom URL.<br>
            2. ➡️ Define table identification options (if needed).<br>
            3. ➡️ Set up file filtering and general keyword options.<br>
            4. ➡️ Select additional filters (year, month).<br>
            5. ➡️ Configure pagination settings (if needed).<br>
            6. ➡️ Click "Extract Data" to start scraping.<br>
            7. ➡️ Review extracted table data and file links.<br>
            8. ➡️ Download files as a ZIP archive.<br>
            9. ➡️ Save or load configurations.<br>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='use-item'>
            <h3>📄 PDF Table Extraction</h3>
            <p>
                1. ➡️ Upload one or more PDF files.<br>
                2. ➡️ Select the extraction engine (Camelot or Tabula-py).<br>
                3. ➡️ Select the extraction method (`lattice` or `stream`).<br>
                4. ➡️ Select the pages to process.<br>
                5. ➡️ Click "Extract Tables".<br>
                6. ➡️ Review, edit, and download the extracted tables in CSV, Excel, or JSON format.<br>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='use-item'>
            <h3>📊 Data Visualization</h3>
            <p>
                1. ➡️ Upload a CSV or Excel file.<br>
                2. ➡️ Adjust column data types as needed.<br>
                3. ➡️ Select a row range for visualization.<br>
                4. ➡️ Choose the type of plot (Histogram, Scatter Plot, Line Chart, or Bar Chart).<br>
                5. ➡️ Customize plot settings.<br>
                6. ➡️ Download the transformed data in CSV format.<br>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='use-item'>
            <h3>🤖 RAG-Powered PDF Insights</h3>
            <p>
                1. ➡️ Upload one or more PDF files.<br>
                2. ➡️ Select a chunking strategy and set chunking parameters.<br>
                3. ➡️ Choose a sentence embedding model.<br>
                4. ➡️ Select a Large Language Model (LLM).<br>
                5. ➡️ Enter your question.<br>
                6. ➡️ Adjust settings (max answer length, confidence threshold).<br>
                7. ➡️ Click "Generate Response" to get the answer and context.<br>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")  # Section separator
    st.markdown(
        """
        <h2 style='color: #2196F3;'>📚 Libraries Used</h2>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .library-item {
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            background-color: #e8f5e9;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-size: 0.9em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='library-item'>
        <b>Streamlit:</b> For building the interactive web application interface.
    </div>
    <div class='library-item'>
        <b>Pandas:</b> For efficient data manipulation and table handling.
    </div>
    <div class='library-item'>
        <b>Camelot:</b> For advanced table extraction from PDF files.
    </div>
    <div class='library-item'>
        <b>Tabula-py:</b> For advanced table extraction from PDF files.
    </div>
    <div class='library-item'>
        <b>Beautiful Soup:</b> For parsing HTML during web scraping.
    </div>
    <div class='library-item'>
        <b>Selenium:</b> For handling dynamic web scraping and browser interactions.
    </div>
    <div class='library-item'>
        <b>PyPDF2:</b> For reading and extracting text from PDF files.
    </div>
    <div class='library-item'>
        <b>requests:</b> For making HTTP requests.
    </div>
    <div class='library-item'>
        <b>sentence_transformers:</b> To create embeddings.
    </div>
    <div class='library-item'>
        <b>transformers:</b> To use LLMs.
    </div>
    <div class='library-item'>
        <b>scikit-learn:</b> To compute cosine_similarity.
    </div>
    <div class='library-item'>
        <b>NLTK:</b> To work with text tokenization.
    </div>
    <div class='library-item'>
        <b>Langchain:</b> For semantic chunking.
    </div>
    <div class='library-item'>
        <b>Altair:</b> For data visualization and creating interactive charts.
    </div>
    <div class='library-item'>
        <b>Others:</b> Various other helpful libraries for specific tasks.
    </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")  # Section separator

    st.markdown(
        """
        <h2 style='color: #2196F3;'>📧 Contact</h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
            <p>
                If you have any questions, feedback, or encounter any issues, please feel free to contact the developer at <a href="mailto:yonas.yigezu@un.org">yonas.yigezu@un.org</a> and <a href="mailto:seidoui@un.org">seidoui@un.org</a>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
