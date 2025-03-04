# scraper/scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from .utils import check_robots_txt  # Assuming check_robots_txt is in utils.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import logging


def detect_column_type(column):
    """Detect the data type of a column."""
    if pd.api.types.is_numeric_dtype(column):
        if all(x % 1 == 0 for x in column if pd.notna(x)):
            return "integer"
        else:
            return "float"
    elif pd.api.types.is_datetime64_any_dtype(column):
        return "datetime"
    else:
        return "string"


def extract_table_data(table_tag, table_id, table_class, table_keyword):
    """Extracts data from a table tag, handling identification heuristics."""

    if table_id and table_tag.get("id") != table_id:
        return None
    if table_class and table_tag.get("class") != [table_class]:
        return None
    if table_keyword:
        if not table_tag.parent or table_keyword.lower() not in table_tag.parent.text.lower():
            return None

    rows = table_tag.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all(["th", "td"])
        data.append([col.get_text(strip=True) for col in cols])

    if not data:
        return None

    df = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame()
    if not df.empty:
        logging.info(f"Found a table with ID: {table_tag.get('id')} , class: {table_tag.get('class')}")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = pd.to_numeric(df[col], errors='ignore')
                if all(isinstance(x, (int, float)) for x in df[col]):
                    continue
                if all(re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(x)) for x in df[col]):
                    df[col] = pd.to_datetime(df[col], errors='coerce')

    return df


def extract_static_data(url: str, table_id="", table_class="", table_keyword="") -> list:
    """
    Extracts tabular data from a static webpage.
    Checks robots.txt and uses BeautifulSoup to parse HTML.
    """
    # Check robots.txt for ethical scraping (commented out for now)
    # if not check_robots_txt(url):
    #     raise Exception("Scraping disallowed by robots.txt.")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table")
    if tables:
        logging.info(f"Found {len(tables)} tables in url:{url}")
        all_tables_data = []
        for table in tables:
            df = extract_table_data(table, table_id, table_class, table_keyword)
            if df is not None and not df.empty:
                all_tables_data.append(df)
        return all_tables_data
    else:
        logging.info(f"No tables found in url: {url}")
        return []


def extract_dynamic_data(url: str, table_id="", table_class="", table_keyword="") -> list:
    """
    Extracts tabular data from a dynamic webpage using Selenium.
    """
    options = Options()
    options.headless = True  # Run in headless mode (no visible browser)
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # Wait for JavaScript to load content (adjust as necessary)
        time.sleep(5)  # Consider using WebDriverWait for more reliable waiting
        page_source = driver.page_source
    except Exception as e:
        logging.error(f"Error during dynamic extraction from {url}: {e}")
        return []
    finally:
        driver.quit()

    # Continue processing with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    tables = soup.find_all("table")
    if tables:
        logging.info(f"Found {len(tables)} tables in url:{url}")
        all_tables_data = []
        for table in tables:
            df = extract_table_data(table, table_id, table_class, table_keyword)
            if df is not None and not df.empty:
                all_tables_data.append(df)
        return all_tables_data
    else:
        logging.info(f"No tables found in url: {url}")
        return []

