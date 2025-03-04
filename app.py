import streamlit as st

st.set_page_config(
    page_title="AI Data Extraction App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from home_page import home_page
from web_scraping_page import web_scraping_page
from pdf_table_extraction_page import pdf_table_extraction_page
from data_visualization_page import data_visualization_page
from pdf_question_answering_page import pdf_question_answering_page
from about_page import about_page

# Sidebar navigation using a selectbox.
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ("Home", "Web Scraping", "PDF Table Extraction", "Data Visualization", 
     "PDF Question-Answering", "Documentation"),
    index=0
)

# Render the selected page.

if page == "Home":
    home_page()
elif page == "Web Scraping":
    web_scraping_page()
elif page == "PDF Table Extraction":
    pdf_table_extraction_page()
elif page == "Data Visualization":
    data_visualization_page()
elif page == "PDF Question-Answering":
    pdf_question_answering_page()
elif page == "Documentation":
    about_page()
