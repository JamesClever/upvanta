def normalize_jsearch_job(job):
    """
    Convert a JSearch job object into Upvanta's standard format.
    """

    return {
        "title": job.get("job_title"),
        "company": job.get("employer_name"),
        "location": job.get("job_location"),
        "salary": job.get("job_salary_string"),
        "description": job.get("job_description"),
        "apply_url": job.get("job_apply_link"),
        "source": "JSearch",
        "posted_at": job.get("job_posted_at"),
        "remote": job.get("job_is_remote", False),
        "verified": bool(job.get("employer_website")),
        "raw": job
    }