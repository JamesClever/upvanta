from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.profile_service import calculate_profile_completion


dashboard = Blueprint(
    "dashboard",
    __name__
)


@dashboard.route("/dashboard")
@login_required
def index():

    stats = {
        "profile": calculate_profile_completion(current_user),
        "jobs": 5,
        "scholarships": 10,
        "courses": 6,
        "mentorships": 3,
        "resumes": 2,
        "saved_jobs": 4
    }

    return render_template(
        "dashboard.html",
        user=current_user,
        stats=stats
    )