"""
Personalized job ranking.

Boost jobs that better match the current user.
"""


def personalization_bonus(job, user):

    if not user:
        return 0

    score = 0

    # -------------------------
    # Preferred Location
    # -------------------------

    preferred_location = getattr(
        user,
        "preferred_location",
        None
    )

    if preferred_location:

        location = (
            job.get("location") or ""
        ).lower()

        if preferred_location.lower() in location:
            score += 15

    # -------------------------
    # Remote Preference
    # -------------------------

    wants_remote = getattr(
        user,
        "remote_only",
        False
    )

    if wants_remote:

        title = (
            job.get("title") or ""
        ).lower()

        description = (
            job.get("description") or ""
        ).lower()

        if "remote" in title or "remote" in description:
            score += 20

    return score