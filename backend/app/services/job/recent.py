from datetime import datetime


def recent_bonus(job):
    """
    Reward recently posted jobs.
    """

    date = job.get("date_posted")

    if not date:
        return 0

    try:

        if isinstance(date, str):
            date = datetime.fromisoformat(
                date.replace("Z", "")
            )

        age = (
            datetime.utcnow() - date
        ).days

    except Exception:
        return 0

    if age <= 1:
        return 20

    if age <= 3:
        return 15

    if age <= 7:
        return 10

    if age <= 30:
        return 5

    return 0