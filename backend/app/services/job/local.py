from app.models import Job


def search_local_jobs(query):
    """
    Search jobs stored in the Upvanta database.
    """

    jobs = Job.query.filter(
        Job.title.ilike(f"%{query}%")
    ).all()

    results = []

    for job in jobs:
        results.append({
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary": job.salary,
            "description": job.description,
            "apply_url": None,
            "source": "Local",
            "posted_at": None,
            "remote": False,
            "verified": True,
            "raw": job
        })

    return results