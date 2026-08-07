from .keywords import KEYWORDS


def semantic_bonus(job, query):
    """
    Reward jobs that match related technologies.
    """

    query = query.lower()

    related = KEYWORDS.get(
        query,
        [query]
    )

    text = " ".join([

        job.get("title", ""),
        job.get("description", ""),
        job.get("company", "")

    ]).lower()

    score = 0

    for word in related:

        if word.lower() in text:
            score += 5

    return score