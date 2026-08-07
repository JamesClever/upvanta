from .local import search_local_jobs
from .jsearch import search_jsearch_jobs
from .adzuna import search_adzuna_jobs
from .deduplicate import remove_duplicates
from .ranking import rank_jobs


def search_jobs(query, user=None):

    local_jobs = search_local_jobs(query)
    print(f"Local Jobs: {len(local_jobs)}")

    jsearch_jobs = search_jsearch_jobs(query)
    print(f"JSearch Jobs: {len(jsearch_jobs)}")

    adzuna_jobs = search_adzuna_jobs(query)
    print(f"Adzuna Jobs: {len(adzuna_jobs)}")

    jobs = (
        local_jobs +
        jsearch_jobs +
        adzuna_jobs
    )

    print(f"Combined Jobs: {len(jobs)}")

    jobs = remove_duplicates(jobs)

    print(f"After Deduplication: {len(jobs)}")

    jobs = rank_jobs(
        jobs,
        query,
        user
    )

    return jobs