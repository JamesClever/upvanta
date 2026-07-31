from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

from app.services.career_progress_service import calculate_career_progress


dashboard = Blueprint(
    "dashboard",
    __name__
)


@dashboard.route("/dashboard")
@login_required
def index():

    # PROFILE PROGRESS

    progress = calculate_career_progress(
        current_user
    )

    profile_progress = progress["profile_progress"]

    resume_progress = progress["resume_progress"]

    jobs_progress = progress["jobs_progress"]

    jobs_count = progress["jobs_count"]



    stats = {
        "profile": profile_progress,
        "jobs": progress["jobs_count"],
        "courses": progress["courses_count"],
        "scholarships": progress["scholarships_count"],
        "mentorships": progress["mentorship_count"],
        "career_score": progress["career_score"]
    }

    

    current_date = datetime.now().strftime("%A, %d %B %Y")

    return render_template(

    "dashboard.html",

    user=current_user,

    stats=stats,

    profile_progress=profile_progress,

    resume_progress=resume_progress,

    jobs_progress=jobs_progress,

    jobs_count=jobs_count,

    courses_count=progress["courses_count"],

    scholarships_count=progress["scholarships_count"],

    mentorship_count=progress["mentorship_count"],

    career_score=progress["career_score"],

    current_date=current_date

)