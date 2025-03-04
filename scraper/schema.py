# scraper/schema.py
import json

def parse_schema(schema_str: str) -> dict:
    """
    Parses a JSON-like schema provided by the user.
    Expected format:
    {
        "keywords": ["population", "GDP", "unemployment"],
        "file_name": "stats_2025",
        "data_types": {
            "population": "integer",
            "GDP": "float",
            "unemployment": "float"
        }
    }
    """
    try:
        schema = json.loads(schema_str)
        return schema
    except Exception as e:
        raise ValueError("Invalid JSON schema provided.") from e

