from app.extensions import db
from app.models.resume.resume import Resume


def calculate_resume_completion(resume):

    if resume is None:
        return 0

    fields = [
        resume.full_name,
        resume.email,
        resume.phone,
        resume.location,
        resume.education,
        resume.experience,
        resume.skills,
        resume.summary,
    ]

    completed = sum(
        1 for field in fields
        if field and str(field).strip()
    )

    return round(completed / len(fields) * 100)


def sync_resume_from_profile(user):
    """
    Synchronize profile information into the user's resume.

    Existing resume data is never overwritten.
    Empty resume fields are automatically populated
    from the user's profile.
    """

    resume = Resume.query.filter_by(
        user_id=user.id
    ).first()

    # ----------------------------------
    # Create resume if it doesn't exist
    # ----------------------------------

    if resume is None:

        resume = Resume(
            user_id=user.id,
            full_name=user.full_name or "",
            email=user.email or "",
            phone="",
            location=user.location or "",
            education=user.education or "",
            experience=user.experience or "",
            skills=user.skills or "",
            summary=""
        )

        db.session.add(resume)
        db.session.commit()

        return resume

    # ----------------------------------
    # Only fill missing fields
    # ----------------------------------

    if not resume.full_name:
        resume.full_name = user.full_name

    if not resume.email:
        resume.email = user.email

    if not resume.location:
        resume.location = user.location

    if not resume.education:
        resume.education = user.education

    if not resume.experience:
        resume.experience = user.experience

    if not resume.skills:
        resume.skills = user.skills

    db.session.commit()

    return resume