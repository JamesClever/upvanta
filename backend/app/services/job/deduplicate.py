def remove_duplicates(jobs):
    seen = set()
    unique_jobs = []

    for job in jobs:
        key = (
            (job.get("title") or "").lower().strip(),
            (job.get("company") or "").lower().strip(),
            (job.get("location") or "").lower().strip()
        )

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs