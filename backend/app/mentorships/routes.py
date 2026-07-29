from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.mentorship import Mentorship
from app.forms.mentorship_form import MentorshipForm
from app.extensions import db


mentorships = Blueprint(
    "mentorships",
    __name__
)

@mentorships.route("/mentorships")
def list_mentorships():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = Mentorship.query

    if search:
        query = query.filter(
            Mentorship.mentor.ilike(f"%{search}%")
        )

    mentorships = query.order_by(
        Mentorship.id.desc()
    ).paginate(
        page=page,
        per_page=12,
        error_out=False
    )

    return render_template(
        "mentorships/mentorships.html",
        mentorships=mentorships,
        search=search
    )

@mentorships.route("/mentorships/add", methods=["GET", "POST"])
def add_mentorship():

    form = MentorshipForm()

    if form.validate_on_submit():

        mentorship = Mentorship(
            mentor=form.mentor.data,
            expertise=form.expertise.data,
            organization=form.organization.data,
            location=form.location.data,
            availability=form.availability.data,
            description=form.description.data
        )

        db.session.add(mentorship)
        db.session.commit()

        flash(
            "Mentorship added successfully!",
            "success"
        )

        return redirect(
            url_for("mentorships.list_mentorships")
        )

    return render_template(
        "mentorships/add_mentorship.html",
        form=form
    )


@mentorships.route("/mentorships/<int:mentorship_id>")
def mentorship_details(mentorship_id):

    mentorship = Mentorship.query.get_or_404(
        mentorship_id
    )

    return render_template(
        "mentorships/details.html",
        mentorship=mentorship
    )


@mentorships.route("/mentorships/<int:mentorship_id>/edit", methods=["GET", "POST"])
def edit_mentorship(mentorship_id):

    mentorship = Mentorship.query.get_or_404(
        mentorship_id
    )

    form = MentorshipForm(obj=mentorship)

    if form.validate_on_submit():

        mentorship.mentor = form.mentor.data
        mentorship.expertise = form.expertise.data
        mentorship.organization = form.organization.data
        mentorship.location = form.location.data
        mentorship.availability = form.availability.data
        mentorship.description = form.description.data

        db.session.commit()

        flash(
            "Mentorship updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "mentorships.mentorship_details",
                mentorship_id=mentorship.id
            )
        )

    return render_template(
        "mentorships/edit_mentorship.html",
        form=form,
        mentorship=mentorship
    )


@mentorships.route("/mentorships/<int:mentorship_id>/delete", methods=["POST"])
def delete_mentorship(mentorship_id):

    mentorship = Mentorship.query.get_or_404(
        mentorship_id
    )

    db.session.delete(mentorship)
    db.session.commit()

    flash(
        "Mentorship deleted successfully!",
        "success"
    )

    return redirect(
        url_for("mentorships.list_mentorships")
    )