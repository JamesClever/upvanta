from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.services.image_service import save_profile_picture


profile = Blueprint(
    "profile",
    __name__
)


@profile.route("/profile", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

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

        db.session.commit()

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