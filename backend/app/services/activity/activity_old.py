from flask import Blueprint, render_template, redirect, url_for, flash, request

from flask_login import login_required, current_user

from app.models.scholarship import Scholarship
from app.models.saved_scholarship import SavedScholarship
from app.models.scholarship_application import ScholarshipApplication

from app.forms.scholarship_form import ScholarshipForm

from app.services.activity_service import create_activity

from app.extensions import db


scholarships = Blueprint(
    "scholarships",
    __name__
)


# ==========================================
# LIST SCHOLARSHIPS
# ==========================================

@scholarships.route("/scholarships")
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


    scholarships_list = query.order_by(
        Scholarship.id.desc()
    ).paginate(
        page=page,
        per_page=12
    )


    return render_template(
        "scholarships/scholarships.html",
        scholarships=scholarships_list,
        search=search
    )



# ==========================================
# SCHOLARSHIP DETAILS
# ==========================================

@scholarships.route(
    "/scholarships/<int:scholarship_id>"
)
def scholarship_details(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )


    return render_template(
        "scholarships/details.html",
        scholarship=scholarship
    )



# ==========================================
# SAVE SCHOLARSHIP
# ==========================================

@scholarships.route(
    "/scholarships/<int:scholarship_id>/save",
    methods=["POST"]
)
@login_required
def save_scholarship(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )


    existing = SavedScholarship.query.filter_by(
        user_id=current_user.id,
        scholarship_id=scholarship.id
    ).first()


    if existing:

        flash(
            "Scholarship already saved.",
            "info"
        )


    else:

        saved = SavedScholarship(
            user_id=current_user.id,
            scholarship_id=scholarship.id
        )


        db.session.add(
            saved
        )

        db.session.commit()


        create_activity(
            current_user,
            icon="🎓",
            title="Scholarship Saved",
            url=url_for(
                "scholarships.scholarship_details",
                scholarship_id=scholarship.id
            ),
            module="scholarships"
        )


        flash(
            "Scholarship saved successfully!",
            "success"
        )


    return redirect(
        url_for(
            "scholarships.scholarship_details",
            scholarship_id=scholarship.id
        )
    )



# ==========================================
# APPLY FOR SCHOLARSHIP
# ==========================================

@scholarships.route(
    "/scholarships/<int:scholarship_id>/apply",
    methods=["POST"]
)
@login_required
def apply_scholarship(scholarship_id):

    scholarship = Scholarship.query.get_or_404(
        scholarship_id
    )


    existing = ScholarshipApplication.query.filter_by(
        user_id=current_user.id,
        scholarship_id=scholarship.id
    ).first()


    if existing:

        flash(
            "You already applied for this scholarship.",
            "info"
        )


    else:

        application = ScholarshipApplication(
            user_id=current_user.id,
            scholarship_id=scholarship.id,
            status="Submitted"
        )


        db.session.add(
            application
        )


        db.session.commit()


        create_activity(
            current_user,
            icon="🎓",
            title="Scholarship Application Submitted",
            url=url_for(
                "scholarships.scholarship_details",
                scholarship_id=scholarship.id
            ),
            module="scholarships"
        )


        flash(
            "Scholarship application submitted!",
            "success"
        )


    return redirect(
        url_for(
            "scholarships.scholarship_details",
            scholarship_id=scholarship.id
        )
    )



# ==========================================
# ADD SCHOLARSHIP
# ==========================================

@scholarships.route(
    "/scholarships/add",
    methods=["GET", "POST"]
)
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


        db.session.add(
            scholarship
        )

        db.session.commit()


        flash(
            "Scholarship added successfully!",
            "success"
        )


        return redirect(
            url_for(
                "scholarships.list_scholarships"
            )
        )


    return render_template(
        "scholarships/add_scholarship.html",
        form=form
    )



# ==========================================
# EDIT SCHOLARSHIP
# ==========================================

@scholarships.route(
    "/scholarships/<int:scholarship_id>/edit",
    methods=["GET", "POST"]
)
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



# ==========================================
# DELETE SCHOLARSHIP
# ==========================================

@scholarships.route(
    "/scholarships/<int:scholarship_id>/delete",
    methods=["POST"]
)
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