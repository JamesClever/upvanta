"""
Normalize job data from different providers
into one common structure.
"""


def normalize_jsearch(job):

    return {

        "title": job.get("job_title"),

        "company": job.get("employer_name"),

        "location": " ".join(
            filter(
                None,
                [
                    job.get("job_city"),
                    job.get("job_country")
                ]
            )
        ),

        "salary": job.get("salary"),

        "description": job.get("job_description"),

        "apply_link": job.get("job_apply_link"),

        "posted_at": job.get("job_posted_at_datetime_utc"),

        "source": "jsearch"

    }


def normalize_adzuna(job):

    company = ""

    if job.get("company"):

        company = job["company"].get(
            "display_name",
            ""
        )

    location = ""

    if job.get("location"):

        location = job["location"].get(
            "display_name",
            ""
        )

    return {

        "title": job.get("title"),

        "company": company,

        "location": location,

        "salary": job.get("salary_max"),

        "description": job.get("description"),

        "apply_link": job.get("redirect_url"),

        "posted_at": job.get("created"),

        "source": "adzuna"

    }