from datetime import datetime

from app.extensions import db
from app.models.job.job_application import JobApplication
from app.models.resume import Resume


def apply_for_job(user, job):
    """
    Apply the logged-in user to a job.
    Returns the existing application if one already exists.
    """

    application = JobApplication.query.filter_by(
        user_id=user.id,
        job_id=job.id
    ).first()

    if application:
        return application

    resume = Resume.query.filter_by(
        user_id=user.id
    ).first()

    application = JobApplication(
        user_id=user.id,
        job_id=job.id,
        resume_id=resume.id if resume else None,
        status="Applied",
        applied_at=datetime.utcnow()
    )

    db.session.add(application)
    db.session.commit()

    return application