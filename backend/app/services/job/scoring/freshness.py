from datetime import datetime


def freshness_score(job):
    """
    Reward recently posted jobs.
    """

    date = job.get("date_posted")

    if not date:
        return 0, "No posting date"

    try:

        if isinstance(date, str):
            date = datetime.fromisoformat(
                date.replace("Z", "")
            )

        age = (
            datetime.utcnow() - date
        ).days

    except Exception:
        return 0, "Invalid posting date"

    if age <= 1:
        return 1.0, "Posted today"

    if age <= 3:
        return 0.75, "Posted this week"

    if age <= 7:
        return 0.50, "Posted this week"

    if age <= 30:
        return 0.25, "Posted this month"

    return 0, "Older posting"