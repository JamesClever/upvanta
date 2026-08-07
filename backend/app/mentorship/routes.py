from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.models.mentorship.mentorship import Mentorship
from app.forms.mentorship.form import MentorshipForm
from app.extensions import db


mentorship = Blueprint(
    "mentorship",
    __name__
)


@mentorship.route("/mentorships")
def list_mentorships():

    search = request.args.get(
        "search",
        ""
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = Mentorship.query

    if search:

        query = query.filter(
            Mentorship.mentor.ilike(
                f"%{search}%"
            )
        )

    mentorships = (
        query
        .order_by(
            Mentorship.id.desc()
        )
        .paginate(
            page=page,
            per_page=12,
            error_out=False
        )
    )

    return render_template(
        "mentorship/list.html",
        mentorships=mentorships,
        search=search
    )


@mentorship.route(
    "/mentorships/add",
    methods=["GET", "POST"]
)
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

        db.session.add(
            mentorship
        )

        db.session.commit()

        flash(
            "Mentorship added successfully!",
            "success"
        )

        return redirect(
            url_for(
                "mentorship.list_mentorships"
            )
        )

    return render_template(
        "mentorship/add.html",
        form=form
    )


@mentorship.route("/mentorships/<int:mentorship_id>")
def mentorship_details(mentorship_id):

    mentorship = Mentorship.query.get_or_404(
        mentorship_id
    )

    return render_template(
        "mentorship/details.html",
        mentorship=mentorship
    )


@mentorship.route(
    "/mentorships/<int:mentorship_id>/edit",
    methods=["GET", "POST"]
)
def edit_mentorship(mentorship_id):

    mentorship = Mentorship.query.get_or_404(
        mentorship_id
    )

    form = MentorshipForm(
        obj=mentorship
    )

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
                "mentorship.mentorship_details",
                mentorship_id=mentorship.id
            )
        )

    return render_template(
        "mentorship/edit.html",
        form=form,
        mentorship=mentorship
    )


@mentorship.route(
    "/mentorships/<int:mentorship_id>/delete",
    methods=["POST"]
)
def delete_mentorship(mentorship_id):

    mentorship = Mentorship.query.get_or_404(
        mentorship_id
    )

    db.session.delete(
        mentorship
    )

    db.session.commit()

    flash(
        "Mentorship deleted successfully!",
        "success"
    )

    return redirect(
        url_for(
            "mentorship.list_mentorships"
        )
    )