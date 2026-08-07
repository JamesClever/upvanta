import os
import requests


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def search_adzuna_jobs(query):

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return []

    url = (
        "https://api.adzuna.com/v1/api/jobs/us/search/1"
    )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 20,
        "what": query,
        "content-type": "application/json"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        print(response.status_code)
        print(response.url)
        print(response.text)

        response.raise_for_status()

        data = response.json()

        jobs = []

        for item in data.get("results", []):

            jobs.append({

                "id": item.get("id"),

                "title": item.get("title"),

                "company": (
                    item.get("company") or {}
                ).get("display_name"),

                "location": (
                    item.get("location") or {}
                ).get("display_name"),

                "salary": item.get("salary_max"),

                "description": item.get("description"),

                "apply_url": item.get("redirect_url"),

                "source": "Adzuna"

            })

        print(f"Adzuna returned {len(jobs)} jobs")

        return jobs

    except Exception as e:
        print("Adzuna Error:", e)

        if 'response' in locals():
            print(response.text)

        return []