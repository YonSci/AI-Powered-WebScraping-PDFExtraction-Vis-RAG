# scraper/utils.py
import streamlit as st
from urllib.parse import urljoin
import requests
import logging
import pandas as pd
from bs4 import BeautifulSoup
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import os


def check_robots_txt(url: str) -> bool:
    """
    Checks if the website's robots.txt permits scraping.
    A simple check is performed (this can be enhanced with a full parser).
    """
    robots_url = urljoin(url, "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            # Basic check: if "Disallow: /" is present, block scraping
            if "Disallow: /" in response.text:
                return False
        return True
    except Exception:
        # If robots.txt is unreachable, default to disallowing scraping.
        return False
    

# Utility functions (could be moved to utils.py)
def is_file_link(url):
    file_extensions = [".pdf", ".csv", ".xls", ".xlsx", ".json"]
    return any(url.lower().endswith(ext) for ext in file_extensions)

def create_session_with_retry():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429,500,502,503,504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def download_file(url):
    session = create_session_with_retry()
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading file from {url}: {e}")
        logging.error(f"Error downloading file from {url}: {e}")
        return None
    finally:
        session.close()

def extract_file_links(page_url, extensions, file_name_contains_all, query_keywords_all, query_keywords_any, custom_file_name, custom_keywords, custom_file_type):
    # Robust error handling, logging and returning empty list on failure.
    session = create_session_with_retry()
    try:
        response = session.get(page_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        st.error(f"Error accessing {page_url}: {e}")
        logging.error(f"Error accessing {page_url}: {e}")
        return []
    finally:
        session.close()
    
    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        for ext in extensions:
            if href.lower().endswith(ext):
                full_url = urljoin(page_url, href)
                file_name = full_url.split("/")[-1].split("?")[0]
                if custom_keywords:
                    custom_keywords_list = [kw.strip() for kw in custom_keywords.split(',')] if custom_keywords else []
                else:
                    custom_keywords_list = []
                valid_custom_name = not custom_file_name or custom_file_name.lower() in file_name.lower()
                valid_custom_keywords = not custom_keywords or any(kw.lower() in file_name.lower() for kw in custom_keywords_list)
                valid_file_type = not custom_file_type or any(file_name.lower().endswith(ft.lower()) for ft in custom_file_type)
                if valid_custom_name and valid_custom_keywords and valid_file_type:
                    links.append(full_url)
                elif file_name_contains_all and query_keywords_all and not (valid_custom_name or valid_custom_keywords or valid_file_type):
                    if all(kw.lower() in file_name.lower() for kw in query_keywords_all):
                        links.append(full_url)
                elif not file_name_contains_all and query_keywords_any and not (valid_custom_name or valid_custom_keywords or valid_file_type):
                    if any(kw.lower() in file_name.lower() for kw in query_keywords_any):
                        links.append(full_url)

                break
    return links

def extract_paginated_data(base_url, max_pages=5, table_id="", table_class="", table_keyword=""):
    session = create_session_with_retry()
    all_tables_data = []
    next_url = base_url
    page_count = 0
    progress_bar = st.progress(0, text="Scraping pages...")
    while next_url and page_count < max_pages:
        try:
            response = session.get(next_url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            st.error(f"Timeout error accessing {next_url}: {e}")
            logging.error(f"Timeout error accessing {next_url}: {e}")
            break
        except requests.exceptions.RequestException as e:
            st.error(f"Error accessing {next_url}: {e}")
            logging.error(f"Error accessing {next_url}: {e}")
            break
        except Exception as e:
            st.error(f"Error parsing HTML from {next_url}: {e}")
            logging.error(f"Error parsing HTML from {next_url}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            from scraper.scraper import extract_table_data
            tables = soup.find_all("table")
            for table_tag in tables:
                df = extract_table_data(table_tag, table_id, table_class, table_keyword)
                if df is not None and not df.empty:
                    all_tables_data.append(df)
            
            next_link = soup.find("a", string="Next")
            
            if next_link and next_link.get("href"):
                next_url = urljoin(next_url, next_link["href"])
                page_count += 1
            elif not next_link:
                # Look for page numbers
                possible_pages = [a for a in soup.find_all("a", href=True) if a.text.isdigit()]
                if possible_pages:
                    # Get the highest page number
                    highest_page = max(int(a.text) for a in possible_pages)
                    current_page = page_count + 1
                    # If current page is lower than the highest page then the next url is found
                    if current_page < highest_page:
                        next_url = urljoin(base_url, possible_pages[-1]["href"]) # Get the highest url page number
                        page_count+=1
                    else:
                         next_url=None
                else:
                    next_url = None
            
            
            progress_bar.progress(page_count / max_pages, text=f"Scraping page : {next_url}")
           
            
        except Exception as e:
            st.error(f"Error parsing HTML from {next_url}: {e}")
            logging.error(f"Error parsing HTML from {next_url}: {e}")
            break
        
        finally:
            session.close()
    return all_tables_data

def extract_all_data(url_list, query_keywords_all, query_keywords_any, file_name_contains_all, enable_pagination, max_pages, custom_file_name, custom_keywords, custom_file_type, use_dynamic_content, table_id="", table_class="", table_keyword="", table_progress_bar = None, file_progress_bar=None, progress_text=None):
    if not url_list:
        st.error("Please select a valid url before extraction.")
        return None, None

    all_table_data = []
    all_file_links = []
    
    total_urls = len(url_list)
    table_progress_increment = 1.0 / total_urls if total_urls > 0 else 0
    file_progress_increment = 1.0 / total_urls if total_urls > 0 else 0
    current_table_progress = 0.0
    current_file_progress = 0.0

    for index, url in enumerate(url_list):
        progress_text.text(f"Processing {url}")
        logging.info(f"Processing {url}")
        if is_file_link(url):
            all_file_links.append(url)
        else:
            from scraper.scraper import extract_static_data, extract_dynamic_data
            try:
                if use_dynamic_content:
                    table_data = extract_dynamic_data(url, table_id=table_id, table_class=table_class, table_keyword=table_keyword)
                    if table_data:
                        logging.info(f"Tables found in url: {url}")
                        logging.info(f"Adding tables to all_table_data")
                        all_table_data.extend(table_data)
                else:
                    if enable_pagination:
                        table_data = extract_paginated_data(url, max_pages, table_id=table_id, table_class=table_class, table_keyword=table_keyword)
                        if table_data:
                            logging.info(f"Tables found in url: {url}")
                            logging.info(f"Adding tables to all_table_data")
                            all_table_data.extend(table_data)
                    else:
                        table_data = extract_static_data(url, table_id=table_id, table_class=table_class, table_keyword=table_keyword)
                        if table_data:
                            logging.info(f"Tables found in url: {url}")
                            logging.info(f"Adding tables to all_table_data")
                            all_table_data.extend(table_data)

                # Update table progress bar
                current_table_progress += table_progress_increment
                if table_progress_bar:
                    table_progress_bar.progress(current_table_progress, text=f"Processing url {url} for tables")

                file_links = extract_file_links(url, [".pdf", ".csv", ".xls", ".xlsx", ".json"], file_name_contains_all, query_keywords_all, query_keywords_any, custom_file_name, custom_keywords, custom_file_type)
                logging.info(f"Found {len(file_links)} files in url: {url}")
                all_file_links.extend(file_links)
                
                # Update file progress bar
                current_file_progress += file_progress_increment
                if file_progress_bar:
                    file_progress_bar.progress(current_file_progress, text=f"Processing url {url} for files")
            except Exception as e:
                st.error(f"An error occurred when scraping url {url}: {e}")
                logging.error(f"An error occurred when scraping url {url}: {e}")
                continue
    combined_table = pd.concat(all_table_data, ignore_index=True) if all_table_data else None
    # Process file links applying keyword filtering.
    files = []
    idx = 1
    for link in all_file_links:
        file_name = link.split("/")[-1].split("?")[0]
        file_ext = file_name.split(".")[-1] if "." in file_name else ""
        files.append({
            "No": idx,
            "File Extension": file_ext.upper(),
            "File Name": file_name,
            "URL": link
        })
        idx += 1
    return combined_table, files



def save_config(config_data):
    filename = f"extraction_config_{config_data['selected_country']}.json" if config_data['selected_country'] else "extraction_config.json"
    """Saves extraction configuration to a JSON file."""
    filepath = os.path.join(os.getcwd(), "extraction_configs", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Create directory if it doesn't exist
    try:
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=4)
            st.success(f"Configuration saved to '{filename}' successfully!")
    except Exception as e:
        st.error(f"Error saving configuration: {e}")


def load_config(filename):
    """Loads extraction configuration from a JSON file."""
    filepath = os.path.join(os.getcwd(), "extraction_configs", filename)
    try:
        with open(filepath, 'r') as f:
            config_data = json.load(f)
        return config_data
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return None
