from .scoring.intelligence import score_job


def rank_jobs(jobs, query, user=None):

    ranked = []

    for job in jobs:

        result = score_job(
            job,
            query,
            user
        )

        job["score"] = result["score"]

        job["match"] = result["match"]

        job["reasons"] = result["reasons"]

        ranked.append(job)

    ranked.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return ranked