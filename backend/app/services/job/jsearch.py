import os
import requests
from dotenv import load_dotenv

from .normalizer import normalize_jsearch_job

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

URL = "https://jsearch.p.rapidapi.com/search"


def search_jsearch_jobs(query, page=1):
    """
    Search live jobs from JSearch.
    """

    if not RAPIDAPI_KEY:
        print("RAPIDAPI_KEY is missing")
        return []

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": page,
        "num_pages": 1
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json().get("data", [])

        return [
            normalize_jsearch_job(job)
            for job in data
        ]

    except Exception as e:
        print(f"JSearch error: {e}")
        return []