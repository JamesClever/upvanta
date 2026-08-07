from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)

from flask_login import (
    login_required,
    current_user,
)

from app.extensions import db

from app.models.scholarship.scholarship import Scholarship
from app.models.scholarship.saved import SavedScholarship
from app.models.scholarship.application import ScholarshipApplication

from app.forms.scholarship.form import ScholarshipForm

from app.services.activity.activity import create_activity


scholarship = Blueprint(
    "scholarship",
    __name__
)


@scholarship.route("/scholarships")
def list_scholarships():

    search = request.args.get(
        "search",
        ""
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = Scholarship.query

    if search:

        query = query.filter(
            Scholarship.title.contains(search)
        )

    scholarships = (
        query
        .order_by(
            Scholarship.id.desc()
        )
        .paginate(
            page=page,
            per_page=12
        )
    )

    return render_template(
        "scholarship/list.html",
        scholarships=scholarships,
        search=search
    )


@scholarship.route(
    "/scholarships/add",
    methods=["GET", "POST"]
)
def add_scholarship():

    form = ScholarshipForm()

    if form.validate_on_submit():

        scholarship_item = Scholarship(
            title=form.title.data,
            organization=form.organization.data,
            country=form.country.data,
            level=form.level.data,
            deadline=form.deadline.data,
            amount=form.amount.data,
            description=form.description.data
        )

        db.session.add(scholarship_item)
        db.session.commit()

        flash(
            "Scholarship added successfully!",
            "success"
        )

        return redirect(
            url_for("scholarship.list_scholarships")
        )

    return render_template(
        "scholarship/add.html",
        form=form
    )


@scholarship.route("/scholarships/<int:scholarship_id>")
def scholarship_details(scholarship_id):

    scholarship_item = Scholarship.query.get_or_404(
        scholarship_id
    )

    return render_template(
        "scholarship/details.html",
        scholarship=scholarship_item
    )


@scholarship.route(
    "/scholarships/<int:scholarship_id>/edit",
    methods=["GET", "POST"]
)
def edit_scholarship(scholarship_id):

    scholarship_item = Scholarship.query.get_or_404(
        scholarship_id
    )

    form = ScholarshipForm(
        obj=scholarship_item
    )

    if form.validate_on_submit():

        scholarship_item.title = form.title.data
        scholarship_item.organization = form.organization.data
        scholarship_item.country = form.country.data
        scholarship_item.level = form.level.data
        scholarship_item.deadline = form.deadline.data
        scholarship_item.amount = form.amount.data
        scholarship_item.description = form.description.data

        db.session.commit()

        flash(
            "Scholarship updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "scholarship.scholarship_details",
                scholarship_id=scholarship_item.id
            )
        )

    return render_template(
        "scholarship/edit.html",
        form=form,
        scholarship=scholarship_item
    )


@scholarship.route(
    "/scholarships/<int:scholarship_id>/delete",
    methods=["POST"]
)
def delete_scholarship(scholarship_id):

    scholarship_item = Scholarship.query.get_or_404(
        scholarship_id
    )

    db.session.delete(scholarship_item)
    db.session.commit()

    flash(
        "Scholarship deleted successfully!",
        "success"
    )

    return redirect(
        url_for(
            "scholarship.list_scholarships"
        )
    )