from .company import company_score
from .description import description_score
from .freshness import freshness_score
from .personalization import personalization_score
from .remote import remote_score
from .resume import resume_score
from .salary import salary_score
from .semantic import semantic_score
from .title import title_score

from .weight import WEIGHTS


def score_job(job, query, user=None):
    """
    Returns a complete intelligence report for a job.
    """

    title, title_reason = title_score(job, query)

    description, description_reason = description_score(
        job,
        query
    )

    resume, resume_reason = resume_score(
        job,
        user
    )

    semantic, semantic_reason = semantic_score(
        job,
        query
    )

    company, company_reason = company_score(job)

    salary, salary_reason = salary_score(job)

    freshness, freshness_reason = freshness_score(job)

    remote, remote_reason = remote_score(job)

    personalization, personalization_reason = personalization_score(
        job,
        user
    )

    final_score = (
        title * WEIGHTS["title"] +
        description * WEIGHTS["description"] +
        resume * WEIGHTS["resume"] +
        semantic * WEIGHTS["semantic"] +
        company * WEIGHTS["company"] +
        salary * WEIGHTS["salary"] +
        freshness * WEIGHTS["freshness"] +
        remote * WEIGHTS["remote"] +
        personalization * WEIGHTS["personalization"]
    )

    return {

        "score": round(final_score * 100, 2),

        "match": round(final_score * 100),

        "reasons": {

            "title": title_reason,
            "description": description_reason,
            "resume": resume_reason,
            "semantic": semantic_reason,
            "company": company_reason,
            "salary": salary_reason,
            "freshness": freshness_reason,
            "remote": remote_reason,
            "personalization": personalization_reason

        }

    }