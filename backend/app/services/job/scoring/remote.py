def remote_score(job):
    """
    Score remote work availability.
    """

    title = (job.get("title") or "").lower()

    description = (
        job.get("description") or ""
    ).lower()

    remote = job.get("remote", False)

    remote_terms = [
        "remote",
        "work from home",
        "hybrid",
        "telecommute"
    ]

    if remote:
        return 1.0, "Remote job"

    for term in remote_terms:

        if term in title:

            return 1.0, f"{term.title()} in title"

        if term in description:

            return 0.8, f"{term.title()} in description"

    return 0.0, "On-site"