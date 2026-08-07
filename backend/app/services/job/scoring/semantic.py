from ..keywords import KEYWORDS


def semantic_score(job, query):
    """
    Semantic similarity score.
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


    normalized = min(score / 20, 1.0)


    return normalized, "Semantic relevance"