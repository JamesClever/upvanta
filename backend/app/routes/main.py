from flask import Blueprint, render_template

from app.models import Job
from app.models import Scholarship

main = Blueprint("main", __name__)


@main.route("/")
def home():

    stats = {
        "jobs": Job.query.count(),
        "scholarships": Scholarship.query.count(),
        "countries": 120,   # Placeholder until country data exists
    }

    return render_template(
        "index.html",
        stats=stats
    )