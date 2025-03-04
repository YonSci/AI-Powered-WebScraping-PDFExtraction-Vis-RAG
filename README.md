# Synapse Insights: AI-Powered RAG & Data Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Synapse Insights** is an AI-driven data extraction and analysis application designed to help you unlock valuable insights from diverse data sources, including websites and PDF documents. Leveraging cutting-edge techniques like web scraping, PDF table extraction, interactive data visualization, and Retrieval-Augmented Generation (RAG), Synapse Insights empowers you to transform raw data into actionable intelligence.

## Key Features

*   **🌐 Web Scraping:** Effortlessly extract structured data (tables) and downloadable files from any website.
    *   Support for custom URLs.
    *   Advanced filtering by keywords, file types, years, and months.
    *   Pagination handling for websites with multiple pages of data.
    *   Option to use dynamic web scraping for complex websites.
    *   Save and load configurations for recurring tasks.
*   **📄 PDF Table Extraction:** Intelligently extract tabular data from PDF documents.
    *   Choice between two powerful extraction engines: Camelot and Tabula-py.
    *   Selection of extraction method (lattice or stream) based on the PDF structure.
    *   Interactive table editing to correct errors before export.
    *   Export extracted tables to CSV, Excel, or JSON.
*   **🤖 RAG-Powered PDF Insights:** Engage in natural language question-answering with your PDF documents.
    *   Ask complex questions and receive accurate answers based on the context of your uploaded files.
    *   Multiple chunking strategies (Fixed Size with Overlap, Fixed Size without Overlap, Semantic Chunking with LangChain).
    *   Selection of sentence embedding models for optimal context understanding.
    *   Choice of Large Language Models (LLMs) for question-answering.
    *   View highlighted text in the supporting context.
*   **📊 Interactive Data Visualization:** Explore, transform, and visualize your data with interactive charts and plots.
    *   Upload CSV or Excel files.
    *   Adjust column data types for accurate analysis.
    *   Create histograms, scatter plots, line charts, and bar charts.
    *   Customize chart properties, including axis limits and row selection.
    * Download transformed data.
* **🔄 Configuration Management**: Save and Load configurations for the web scraping tool.
* **💾 Download**: Download files as a ZIP archive.

## Target Audience

Synapse Insights is particularly well-suited for:

*   **National Statistical Offices:** Extract and analyze data for reporting and policymaking.
*   **National Statistical Systems:** Streamline data gathering and processing from various sources.
*   **African Centre for Statistics:** Enhance data-driven decision-making across Africa.
*   **Economic Commission for Africa:** Support economic research and development with advanced data tools.
*   **Data Analysts and Researchers:** Automate data extraction and explore new data sources efficiently.

## Benefits

*   **AI-Powered Efficiency:** Leverage AI to automate complex data extraction and analysis tasks.
*   **Multi-Source Data:** Integrate data from websites and PDFs into a single workflow.
*   **Data-Driven Decision Making:** Gain actionable insights from your data.
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
    git clone <repository-url>
    cd <repository-name>
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions, feedback, or issues, please contact the developer at [yonas.yigezu@un.org](mailto:yonas.yigezu@un.org).

## Collaboration

This tool is developed in collaboration with the **African Centre for Statistics** of the **Economic Commission for Africa**.

