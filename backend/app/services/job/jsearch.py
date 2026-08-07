import os
import requests
from dotenv import load_dotenv

from .normalize import normalize_jsearch

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

URL = "https://jsearch.p.rapidapi.com/search-v2"


def search_jsearch_jobs(query, page=1):
    """
    Search jobs using the JSearch API.
    Returns normalized job dictionaries.
    """

    if not RAPIDAPI_KEY:
        print("RAPIDAPI_KEY missing.")
        return []

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": page,
        "num_pages": 1,
        "country": "us",
        "date_posted": "all"
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json().get("data", {})

        jobs = data.get("jobs", [])

        print(f"JSearch returned {len(jobs)} jobs")

        return [
            normalize_jsearch(job)
            for job in jobs
        ]

    except requests.exceptions.HTTPError as e:
        print("JSearch HTTP Error:", e)
        return []

    except Exception as e:
        print("JSearch Error:", e)
        return []