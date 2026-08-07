from copy import deepcopy

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.services.image.image_service import save_profile_picture
from app.services.resume.builder import sync_resume_from_profile
from app.services.activity.activity import (
    create_activity,
    get_recent_activities,
    profile_snapshot,
)


profile = Blueprint(
    "profile",
    __name__
)


@profile.route("/profile", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        # Take a snapshot before editing
        before = profile_snapshot(current_user)

        # Profile Information
        current_user.bio = request.form.get("bio")
        current_user.location = request.form.get("location")
        current_user.skills = request.form.get("skills")
        current_user.education = request.form.get("education")
        current_user.experience = request.form.get("experience")

        # Profile Picture
        picture = request.files.get("profile_picture")

        if picture and picture.filename:
            filename = save_profile_picture(picture)
            current_user.profile_picture = filename

        # Save profile
        db.session.commit()

        # Synchronize profile to resume
        sync_resume_from_profile(current_user)

        # Take another snapshot after saving
        after = profile_snapshot(current_user)

        # Find what changed
        activities = compare_profile(before, after)

        # Save each activity
        for icon, title in activities:

            create_activity(
                current_user,
                icon=icon,
                title=title,
                url=url_for("profile.index"),
                module="profile"
            )

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("profile.index")
        )

    return render_template(
        "profile/profile.html",
        user=current_user
    )