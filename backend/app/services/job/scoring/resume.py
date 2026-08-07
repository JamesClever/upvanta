"""
Scores how well a user's resume matches a job.
"""


def resume_score(job, user=None):

    if not user:
        return 0, "No resume information"


    score = 0


    job_text = (
        f"{job.get('title', '')} "
        f"{job.get('description', '')}"
    ).lower()


    # -------------------------
    # Skills
    # -------------------------

    skills = getattr(
        user,
        "skills",
        ""
    )

    if skills:

        for skill in skills.split(","):

            skill = skill.strip().lower()

            if skill and skill in job_text:
                score += 8


    # -------------------------
    # Preferred Location
    # -------------------------

    preferred = getattr(
        user,
        "preferred_location",
        ""
    ).lower()


    location = (
        job.get("location") or ""
    ).lower()


    if preferred and preferred in location:
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

        if "remote" in location:
            score += 20

        if "remote" in job_text:
            score += 20


    normalized = min(score / 20, 1.0)

    return normalized, "Resume compatibility"