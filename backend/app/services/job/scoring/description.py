def description_score(job, query):
    """
    Calculate description relevance score.

    Returns:
        score (float): Between 0.0 and 1.0
        reason (str)
    """

    description = (
        job.get("description") or ""
    ).lower()

    query_words = query.lower().split()

    matches = sum(
        1
        for word in query_words
        if word in description
    )

    if not query_words:
        return 0.0, "No search query"

    score = matches / len(query_words)

    return score, (
        f"{matches}/{len(query_words)} keywords matched in description"
    )