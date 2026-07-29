from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.scholarship import Scholarship
from app.forms.scholarship_form import ScholarshipForm
from app.extensions import db


scholarships = Blueprint(
    "scholarships",
    __name__
)

@scholarships.route("/scholarships")
def list_scholarships():

    search = request.args.get("search", "")

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

    scholarships = query.order_by(
        Scholarship.id.desc()
    ).paginate(
        page=page,
        per_page=12
    )

    return render_template(
        "scholarships/scholarships.html",
        scholarships=scholarships,
        search=search
    )


@scholarships.route("/scholarships/add", methods=["GET", "POST"])
def add_scholarship():

    form = ScholarshipForm()

    if form.validate_on_submit():

        scholarship = Scholarship(
            title=form.title.data,
            organization=form.organization.data,
            country=form.country.data,
            level=form.level.data,
            deadline=form.deadline.data,
            amount=form.amount.data,
            description=form.description.data
        )

        db.session.add(scholarship)
        db.session.commit()

        flash(
            "Scholarship added successfully!",
            "success"
        )

        return redirect(
            url_for("scholarships.list_scholarships")
        )


    return render_template(
        "scholarships/add_scholarship.html",
        form=form
    )



@scholarships.route("/scholarships/<int:scholarship_id>")
def scholarship_details(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )

    return render_template(
        "scholarships/details.html",
        scholarship=scholarship
    )



@scholarships.route("/scholarships/<int:scholarship_id>/edit", methods=["GET", "POST"])
def edit_scholarship(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )

    form = ScholarshipForm(
        obj=scholarship
    )


    if form.validate_on_submit():

        scholarship.title = form.title.data
        scholarship.organization = form.organization.data
        scholarship.country = form.country.data
        scholarship.level = form.level.data
        scholarship.deadline = form.deadline.data
        scholarship.amount = form.amount.data
        scholarship.description = form.description.data


        db.session.commit()


        flash(
            "Scholarship updated successfully!",
            "success"
        )


        return redirect(
            url_for(
                "scholarships.scholarship_details",
                scholarship_id=scholarship.id
            )
        )


    return render_template(
        "scholarships/edit_scholarship.html",
        form=form,
        scholarship=scholarship
    )



@scholarships.route("/scholarships/<int:scholarship_id>/delete", methods=["POST"])
def delete_scholarship(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )


    db.session.delete(
        scholarship
    )

    db.session.commit()


    flash(
        "Scholarship deleted successfully!",
        "success"
    )


    return redirect(
        url_for(
            "scholarships.list_scholarships"
        )
    )