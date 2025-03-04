# Synapse Insights: AI-Powered RAG & Data Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This AI-driven data extraction and analysis application designed to help you unlock valuable insights from diverse data sources, including websites and PDF documents. Leveraging cutting-edge techniques like web scraping, PDF table extraction, interactive data visualization, and Retrieval-Augmented Generation (RAG). This AI-powered data tool is developed in collaboration with the *African Centre for Statistics* of the *Economic Commission for Africa*. It aims to enhance data accessibility, extraction, and analysis capabilities for statistical offices and development stakeholders across Africa. Our application empowers you to transform raw data into actionable intelligence using cutting-edge techniques.


## Key Features

**🌐 Web Scraping:** Effortlessly extract and download statistical data (Excel, CSV, PDFs, JSON etc. ) from any website.  

➡️ Select a country or enter a custom URL.  
➡️ Define table identification options (if needed).  
➡️ Set up file filtering and general keyword options.  
➡️ Select additional filters (year, month).  
➡️ Configure pagination settings (if needed).  
➡️ Click "Extract Data" to start scraping.  
➡️ Review extracted table data and file links.  
➡️ Download files as a ZIP archive.  
➡️ Save or load configurations.  


**📄 PDF Table Extraction:** Intelligently extract tabular data from PDF documents.

➡️ Upload one or more PDF files.    
➡️ Select the extraction engine (Camelot or Tabula-py).  
➡️ Select the extraction method (`lattice` or `stream`).  
➡️ Select the pages to process.  
➡️ Click "Extract Tables".  
➡️ Review, edit, and download the extracted tables in CSV, Excel, or JSON format.  

**📊 Interactive Data Visualization:** Explore, transform, and visualize your data with interactive charts and plots.

➡️ Upload a CSV or Excel file.  
➡️ Adjust column data types as needed.  
➡️ Select a row range for visualization.  
➡️ Choose the type of plot (Histogram, Scatter Plot, Line Chart, or Bar Chart).  
➡️ Customize plot settings.  
➡️ Download the transformed data in CSV format.  


**🤖 RAG-Powered PDF Insights:** Engage in natural language question-answering with your PDF documents using Large Language Model (LLM) RAG capabilities.

➡️ Upload one or more PDF files.  
➡️ Select a chunking strategy and set chunking parameters.  
➡️ Choose a sentence embedding model.  
➡️ Select a Large Language Model (LLM).  
➡️ Enter your question.  
➡️ Adjust settings (max answer length, confidence threshold).  
➡️ Click "Generate Response" to get the answer and context.  



## Target Audience

*   **National Statistical Offices:** Extract and analyze data for reporting and policymaking.
*   **National Statistical Systems:** Streamline data gathering and processing from various sources.
*   **African Centre for Statistics:** Enhance data-driven decision-making across Africa.
*   **Economic Commission for Africa:** Support economic research and development with advanced data tools.
*   **Data Analysts and Researchers:** Automate data extraction and explore new data sources efficiently.

## Benefits

*   **AI-Powered Efficiency:** Leverage AI to automate complex data extraction and analysis tasks.
*   **Multi-Source Data:** Integrate data from websites and PDFs into a single workflow.
*   **Interactive Exploration:** Visualize and explore data trends and patterns interactively.
*   **Customizable and Flexible:** Adapt the application to your specific needs with different settings and configurations.
* **User-Friendly**: The tool is user-friendly and easy to use.
* **Transparency**: The tool is transparent.
* **Reproducible**: The steps are reproducible.

## Technologies Used

*   **Streamlit:** For the interactive web application interface.
*   **Pandas:** For data manipulation and analysis.
*   **Camelot, Tabula-py:** For PDF table extraction.
*   **Beautiful Soup, Requests, Selenium:** For web scraping.
*   **PyPDF2:** For PDF text extraction.
*   **Transformers, Sentence Transformers:** For AI/ML models (LLMs, embeddings).
*   **Scikit-learn:** For cosine similarity calculations.
* **NLTK:** for text tokenization.
* **Langchain:** For semantic chunking.
*   **Altair:** For data visualization.
* **Others**: Logging, datetime, os, io, tempfile, re, typing, urllib3, zipfile
* **Custom package**: Scraper

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YonSci/AI-Powered-WebScraping-PDFExtraction-Vis-RAG.git
    cd AI-Powered-WebScraping-PDFExtraction-Vis-RAG
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv aiwebscrp_env
    ```

3. **Activate your env:**
    * **Windows:**

    ```
    .\aiwebscrp_env\Scripts\activate
    ```

    * **macOS/Linux:**

    ```
    source aiwebscrp_env/bin/activate
    ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Run the App**:
    ```
    streamlit run app.py
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contact

For any questions, feedback, or issues, please contact the developer at [yonas.yigezu@un.org](mailto:yonas.yigezu@unorg) & [seidoui@un.org](mailto:seidoui@un.org)

## Collaboration

This tool is developed in collaboration with the **African Centre for Statistics** of the **Economic Commission for Africa**.

