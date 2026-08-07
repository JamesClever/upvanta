from .local import search_local_jobs
from .jsearch import search_jsearch_jobs
from .deduplicate import remove_duplicates
from .ranking import rank_jobs
from .adzuna import search_adzuna_jobs

from .normalizer import normalize_jsearch_job


def search_jobs(query, user=None):
    """
    Search local jobs + live internet jobs,
    remove duplicates, rank them, and return one list.
    """

    local_jobs = search_local_jobs(query)

    # -------------------------
    # JSearch
    # -------------------------

    jsearch_jobs = search_jsearch_jobs(query)

    jsearch_jobs = [
        normalize_jsearch_job(job)
        for job in jsearch_jobs
    ]

    # -------------------------
    # Adzuna
    # -------------------------

    adzuna_jobs = []

    if len(jsearch_jobs) < 10:

        # Already normalized inside search_adzuna_jobs()
        adzuna_jobs = search_adzuna_jobs(query)

    # -------------------------
    # Combine all jobs
    # -------------------------

    jobs = (
        local_jobs +
        jsearch_jobs +
        adzuna_jobs
    )

    jobs = remove_duplicates(jobs)

    jobs = rank_jobs(
        jobs,
        query,
        user
    )

    return jobs