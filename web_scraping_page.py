import streamlit as st
import pandas as pd
import datetime
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scraper.scraper import extract_static_data, extract_dynamic_data
from scraper.utils import is_file_link, create_session_with_retry, download_file, extract_file_links, extract_paginated_data, extract_all_data
import io
import zipfile
from config import CATEGORIES_LIST, COUNTRY_URLS
import logging
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import os

# Configure logging
logging.basicConfig(level=logging.ERROR)

def web_scraping_page():
    # Function to initialize or re-initialize session state
    def initialize_session_state(loaded_config=None):
        if loaded_config:
            st.session_state.update(loaded_config)
        else:
            if "custom_url" not in st.session_state:
                st.session_state["custom_url"] = ""
            if "custom_file_name" not in st.session_state:
                st.session_state["custom_file_name"] = ""
            if "custom_file_type" not in st.session_state:
                st.session_state["custom_file_type"] = []
            if "custom_keywords" not in st.session_state:
                st.session_state["custom_keywords"] = ""
            if "query_keywords_all" not in st.session_state:
                st.session_state["query_keywords_all"] = []
            if "query_keywords_any" not in st.session_state:
                st.session_state["query_keywords_any"] = []
            if "selected_years" not in st.session_state:
                st.session_state["selected_years"] = []
            if "selected_months" not in st.session_state:
                st.session_state["selected_months"] = []
            if "table_id" not in st.session_state:
                st.session_state["table_id"] = ""
            if "table_class" not in st.session_state:
                st.session_state["table_class"] = ""
            if "table_keyword" not in st.session_state:
                st.session_state["table_keyword"] = ""
            if "use_dynamic_content" not in st.session_state:
                st.session_state["use_dynamic_content"] = False
            if "selected_country" not in st.session_state:
                st.session_state["selected_country"] = ""
            if "url_list" not in st.session_state:
              st.session_state["url_list"] = []

    # Function to load the config
    def load_config_from_selected_file():
        if "config_file_select" in st.session_state:
            from scraper.utils import load_config
            loaded_config = load_config(st.session_state["config_file_select"])
            if loaded_config is not None:
                st.session_state.clear()
                initialize_session_state(loaded_config)
                st.rerun()
            else:
                st.error("⚠️ Failed to load configuration.")

    # Flag to request configuration loading
    if "load_config_requested" not in st.session_state:
        st.session_state["load_config_requested"] = False

    # Load config if requested (this happens BEFORE any widgets are created)
    if st.session_state.get("load_config_requested"):
      load_config_from_selected_file()
    
    # Initialize session state
    initialize_session_state()

    st.markdown(
    """
    <div style='background-color: #e0f2f7; padding: 20px; border-radius: 10px;'>
        <h1 style='text-align: center; color: #007BFF;'>📊 Web Scraping Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True,
    )

    st.markdown("## 🌐 Extract and Download Statistical Data")
    st.markdown("---")

    def clear_all_inputs():
        # Clear all the input
        st.session_state["custom_url"] = ""
        st.session_state["custom_file_name"] = ""
        st.session_state["custom_file_type"] = []
        st.session_state["custom_keywords"] = ""
        st.session_state["query_keywords_all"] = []
        st.session_state["query_keywords_any"] = []
        st.session_state["selected_years"] = []
        st.session_state["selected_months"] = []
        st.session_state["table_id"] = ""
        st.session_state["table_class"] = ""
        st.session_state["table_keyword"] = ""
        st.session_state["use_dynamic_content"] = False
        st.session_state["selected_country"] = ""
        st.session_state["url_list"] = []
        st.session_state.pop("all_tables_data", None)
        st.session_state.pop("extracted_files", None)


    with st.sidebar:
        st.header("⚙️ Controls")
        if st.button("🔄 Clear All Inputs", type="primary", key="clear_all_button"):
            clear_all_inputs()
           

    st.subheader("1.🌍 Data Source Configuration")

    col1, col2 = st.columns(2)
    with col1:
        config_dir = os.path.join(os.getcwd(), "extraction_configs")
        config_files = [f for f in os.listdir(config_dir) if f.startswith("extraction_config_") and f.endswith(".json")]
        load_config_enabled = st.checkbox("💾 Load from saved configuration", value=False, key="load_config_enabled")
        if not config_files and load_config_enabled:
            st.error("⚠️ No saved configurations found.")
        elif config_files and load_config_enabled:
            selected_file = st.selectbox("📁 Select a configuration file", [""]+ config_files, key="config_file_select", index=0, on_change=load_config_from_selected_file)

            if st.button("📂 Load Configuration",key="Load_Configuration"):
                st.session_state["config_file_select"] = selected_file
                st.session_state["load_config_requested"] = True
                st.rerun()
    with col2:
        st.markdown("---")
    
    # Create the url_list outside the conditional block.
    url_list = []
    if not load_config_enabled:
        # Selection for country URLs or custom URL.
        selected_country = st.selectbox(
            "ℹ️ Select a country or enter a custom URL to begin scraping:", ["", "Custom URL"] + list(COUNTRY_URLS.keys()), key="selected_country", index=0, on_change=None
        )
        
        custom_url = ""
        # Conditional display of custom URL input
        if selected_country == "Custom URL":
            custom_url = st.text_input("Enter a custom URL:", value=st.session_state["custom_url"], key="custom_url")
            use_dynamic_content = st.checkbox("🌐 Use Dynamic Content", value=st.session_state["use_dynamic_content"])
            url_list.append(custom_url)
            selected_country = None
        elif selected_country:
            url_list.extend(COUNTRY_URLS.get(selected_country, []))
            use_dynamic_content = st.checkbox("🌐 Use Dynamic Content", value=st.session_state["use_dynamic_content"])

        if selected_country:
            st.info(f"🔍 URLs being scraped for {selected_country}:")
            for url in COUNTRY_URLS[selected_country]:
                st.write(url)
        elif custom_url:
            st.info(f"🔍 URL being scraped: {custom_url}")
    else:
        # If config is loaded, we're going to get it from the session_state.
        url_list = st.session_state["url_list"]
        use_dynamic_content = st.session_state["use_dynamic_content"]
    st.session_state["url_list"] = url_list
    st.markdown("---")

    st.subheader("2. 🏷️ Table identification (Optional)")
    col1, col2, col3 = st.columns(3)
    with col1:
        table_id = st.text_input("🆔 Table ID (optional):", value=st.session_state["table_id"], key="table_id")
    with col2:
        table_class = st.text_input("🔤 Table class (optional):", value=st.session_state["table_class"],key="table_class")
    with col3:
        table_keyword = st.text_input("🔑 Keyword near the table (optional):", value=st.session_state["table_keyword"], key="table_keyword")
    
    st.markdown("---")
    st.subheader("3.🗂️ File Filtering Options")
    col1, col2 = st.columns(2)
    with col1:
        custom_file_name = st.text_input("🗂️ File Name Contains (partial match):", value=st.session_state["custom_file_name"], key="custom_file_name")
    with col2:
        custom_file_type = st.multiselect("📄File Type", [".csv", ".pdf", ".xls", ".xlsx", ".json"], default=st.session_state["custom_file_type"], key="custom_file_type")

    custom_keywords = st.text_input(
        "🔑 File Name Keywords (comma-separated):",
        value=st.session_state["custom_keywords"],
        key="custom_keywords",
        help="Filter files by these keywords (at least one must match). "
             "Separate multiple keywords with commas (e.g., GDP, population, census).",
    )

    st.markdown("---")
    st.subheader("4. 🔤 General Keywords (Optional)")
    query_keywords_all = st.multiselect(
        "🔑 Select keywords (all must be present):",
        CATEGORIES_LIST, key="query_keywords_all",
        default=st.session_state["query_keywords_all"],
        help="Filter files by these keywords if all are found in the file name.",
    )
    query_keywords_any = st.multiselect(
        "🔑 Select keywords (at least one must be present):",
        CATEGORIES_LIST,
        help="Filter files by these keywords if at least one is found in the file name.", key="query_keywords_any",default=st.session_state["query_keywords_any"]
    )
    file_name_contains_all = st.checkbox("📄File Name Contains All Keywords", value=False)
    
    st.markdown("---")
    st.subheader("5. 🗓️ Additional Filters (Optional)")
    col1, col2 = st.columns(2)
    with col1:
        current_year = datetime.datetime.now().year
        years = [str(year) for year in range(2000, current_year + 1)]
        selected_years = st.multiselect("🗓️ Select Year", years, help="Filter files by the year in the file name.", key="selected_years", default=st.session_state["selected_years"])
    with col2:
        selected_months = st.multiselect(
            "🗓️ Select Month",
            ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            help="Filter files by the month in the file name.", key="selected_months", default=st.session_state["selected_months"]
        )

    st.markdown("---")
    st.subheader("6. 📃 Pagination Settings")
    enable_pagination = st.checkbox("📃 Enable Pagination", value=False)
    max_pages = st.number_input("🔢 Maximum Pages to Scrape", min_value=1, value=5)

    if st.button("🚀 Start Scraping Data"):
        total_tables_scraped = 0
        total_file_links_found = 0
        extraction_summary = ""
        
        table_progress_bar = st.progress(0, text="🔄 Extracting Table Data...")
        file_progress_bar = st.progress(0, text="🔎 Finding File Links...")
        progress_text = st.empty()

        log_summary = ""

        try:
            combined_tables_all, files = extract_all_data(
                url_list,
                query_keywords_all,
                query_keywords_any,
                file_name_contains_all,
                enable_pagination,
                max_pages,
                custom_file_name,
                custom_keywords,
                custom_file_type,
                use_dynamic_content,
                table_id,
                table_class,
                table_keyword,
                table_progress_bar,
                file_progress_bar,
                progress_text
            )
        except Exception as e:
            st.error(f"⚠️ An error occurred during data extraction: {e}")
            logging.error(f"⚠️ An error occurred during data extraction: {e}")
            return

        if combined_tables_all is not None:
            st.session_state["all_tables_data"] = combined_tables_all
            total_tables_scraped = len(combined_tables_all) if isinstance(combined_tables_all, list) else (combined_tables_all.shape[0] if isinstance(combined_tables_all, pd.DataFrame) else 0)
        else:
            st.session_state["all_tables_data"] = []
            total_tables_scraped = 0

        if files is not None:
            st.session_state["extracted_files"] = files
        else:
            st.session_state["extracted_files"] = []
        
        final_files = files.copy() if files else []
        if selected_years:
            final_files = [f for f in final_files if any(year in f["File Name"] for year in selected_years)]
        if selected_months:
            final_files = [f for f in final_files if any(month.lower() in f["File Name"].lower() for month in selected_months)]
        
        total_file_links_found = len(final_files)
        
        log_summary += f"✅ Scraped {total_tables_scraped} tables.\n"
        log_summary += f"✅ Found {total_file_links_found} file links.\n"
        logging.info(log_summary)

        st.markdown("---")
        st.info(log_summary)
    
    tabs = st.tabs(["📊 Table Data", "📁 File Links & Download"])
    
    st.markdown("---")
    
    with tabs[0]:
        st.subheader("📊 Extracted Table Data")
        all_tables_data = st.session_state.get("all_tables_data", [])
        if all_tables_data:
            for i, df in enumerate(all_tables_data):
                st.markdown(f"**Table {i + 1}**")
                st.dataframe(df)
        else:
            st.info("🔍 No table data found across the pages.")
    
    with tabs[1]:
        st.subheader("📁 Final Extracted Files")
        files = st.session_state.get("extracted_files", [])
        # Apply additional filters: Year and Month.
        final_files = files.copy() if files else []
        if selected_years:
            final_files = [f for f in final_files if any(year in f["File Name"] for year in selected_years)]
        if selected_months:
            final_files = [f for f in final_files if any(month.lower() in f["File Name"].lower() for month in selected_months)]
        
        if final_files:
            final_df = pd.DataFrame(final_files)
            final_df['File Name'] = final_df.apply(
                lambda row: f'<a href="{row["URL"]}" target="_blank">{row["File Name"]}</a>',
                axis=1
            )
            st.markdown(final_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.warning("⚠️ No files match the selected filters.")
        
        if files and final_files:
            folder_name = "_".join(query_keywords_all) if query_keywords_all else "downloaded_files"
            with st.form("download_form"):
                selected_file_names = st.multiselect(
                    "📁 Select files to download",
                    [f["File Name"] for f in final_files],
                    default=st.session_state.get("selected_files", []),
                    key="selected_files_form"
                )
                form_submitted = st.form_submit_button("💾 Generate ZIP")
                if form_submitted:
                    st.session_state["selected_files"] = selected_file_names
                    selected_files = [f for f in final_files if f["File Name"] in selected_file_names]
                    if not selected_files:
                        st.warning("⚠️ No files selected.")
                    else:
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                            for file in selected_files:
                                try:
                                    content = download_file(file["URL"])
                                    if content is not None:
                                        zf.writestr(f"{folder_name}/{file['File Name']}", content)
                                except Exception as e:
                                    st.error(f"⚠️ Error downloading {file['File Name']}: {e}")
                        zip_buffer.seek(0)
                        st.session_state["zip_data"] = zip_buffer.getvalue()
                        st.success("✅ ZIP file generated!")
            
            if st.session_state.get("zip_data") is not None:
                st.download_button(
                    label="📦 Download Selected Files as ZIP",
                    data=st.session_state["zip_data"],
                    file_name=f"{folder_name}.zip",
                    mime="application/zip"
                )
        else:
            st.warning("⚠️ No files available for download based on the selected filters.")
    
    st.subheader("Save Extraction Configuration")
    if st.button("Save Configuration"):
            config_data = {
                "custom_url": st.session_state["custom_url"],
                "selected_country": st.session_state["selected_country"],
                "custom_file_name": st.session_state["custom_file_name"],
                "custom_file_type": st.session_state["custom_file_type"],
                "custom_keywords": st.session_state["custom_keywords"],
                "query_keywords_all": st.session_state["query_keywords_all"],
                "query_keywords_any": st.session_state["query_keywords_any"],
                "selected_years": st.session_state["selected_years"],
                "selected_months": st.session_state["selected_months"],
                "table_id": st.session_state["table_id"],
                "table_class": st.session_state["table_class"],
                "table_keyword": st.session_state["table_keyword"],
                "use_dynamic_content": st.session_state["use_dynamic_content"],
                "url_list": st.session_state["url_list"],
            }
            from scraper.utils import save_config
            save_config(config_data)
