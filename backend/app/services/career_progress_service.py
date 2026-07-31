from app.models.resume import Resume
from app.models.job_application import JobApplication

from app.services.profile_service import calculate_profile_completion
from app.services.resume_service import calculate_resume_completion


def calculate_career_progress(user):

    # ==========================================
    # PROFILE
    # ==========================================

    profile_progress = calculate_profile_completion(
        user
    )

    # ==========================================
    # RESUME
    # ==========================================

    resume = Resume.query.filter_by(
        user_id=user.id
    ).first()

    resume_progress = calculate_resume_completion(
        resume
    )

    # ==========================================
    # JOB APPLICATIONS
    # ==========================================

    jobs_count = JobApplication.query.filter_by(
        user_id=user.id
    ).count()

    jobs_goal = 20

    jobs_progress = min(
        round(jobs_count / jobs_goal * 100),
        100
    )

    # ==========================================
    # PLACEHOLDERS
    # (These will become database queries later)
    # ==========================================

    courses_count = 0
    scholarships_count = 0
    mentorship_count = 0
    ai_sessions = 0

    # ==========================================
    # OVERALL CAREER SCORE
    # ==========================================

    career_score = round(

        (

            profile_progress +

            resume_progress +

            jobs_progress

        ) / 3

    )

    return {

        "profile_progress": profile_progress,

        "resume_progress": resume_progress,

        "jobs_progress": jobs_progress,

        "career_score": career_score,

        "jobs_count": jobs_count,

        "courses_count": courses_count,

        "scholarships_count": scholarships_count,

        "mentorship_count": mentorship_count,

        "ai_sessions": ai_sessions

    }