
# scraper/nlp_parser.py
import spacy

# Load the spaCy model (ensure you have downloaded 'en_core_web_sm')
nlp = spacy.load("en_core_web_sm")

def parse_query(query: str):
    """
    Process the plain English query and extract keywords.
    This could be extended to perform more complex intent recognition.
    """
    doc = nlp(query)
    # Extract nouns and proper nouns as candidate keywords
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return keywords
