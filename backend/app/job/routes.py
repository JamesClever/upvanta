from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db

from app.models import Job, JobApplication

from app.forms.job.form import JobForm

from app.services.job.application import apply_for_job
from app.services.activity.activity import create_activity

from app.services.job.search import search_jobs


job = Blueprint(
    "job",
    __name__
)


@job.route("/jobs")
def list_jobs():

    search = request.args.get(
        "search",
        ""
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    external_jobs = []

    if search:

        jobs = Job.query.filter(
            Job.title.ilike(f"%{search}%")
        ).paginate(
            page=page,
            per_page=12
        )

        # Search internet jobs
        external_jobs = search_jobs(
            search,
            current_user if current_user.is_authenticated else None
        )

    else:

        jobs = Job.query.order_by(
            Job.id.desc()
        ).paginate(
            page=page,
            per_page=12
        )

    return render_template(
        "job/list.html",
        jobs=jobs,
        search=search,
        external_jobs=external_jobs
    )


@job.route("/jobs/<int:job_id>")
def job_details(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    return render_template(
        "job/details.html",
        job=job
    )


# ==========================================
# APPLY FOR JOB
# ==========================================

@job.route(
    "/jobs/<int:job_id>/apply",
    methods=["POST"]
)
@login_required
def apply_job(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    application, created = apply_for_job(
        current_user,
        job
    )

    if created:

        create_activity(
            current_user,
            icon="💼",
            title=f"Applied for {job.title}",
            url=url_for(
                "job.job_details",
                job_id=job.id
            ),
            module="job"
        )

        flash(
            "Application submitted successfully!",
            "success"
        )

    else:

        flash(
            "You've already applied for this job.",
            "info"
        )

    return redirect(
        url_for(
            "job.job_details",
            job_id=job.id
        )
    )


# ==========================================
# ADD JOB
# ==========================================

@job.route(
    "/jobs/add",
    methods=["GET", "POST"]
)
def add_job():

    form = JobForm()

    if form.validate_on_submit():

        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            job_type=form.job_type.data,
            category=form.category.data,
            salary=form.salary.data,
            description=form.description.data
        )

        db.session.add(job)
        db.session.commit()

        flash(
            "Job added successfully!",
            "success"
        )

        return redirect(
            url_for(
                "job.list_jobs"
            )
        )

    return render_template(
        "job/add.html",
        form=form
    )


# ==========================================
# EDIT JOB
# ==========================================

@job.route(
    "/jobs/<int:job_id>/edit",
    methods=["GET", "POST"]
)
def edit_job(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    form = JobForm(
        obj=job
    )

    if form.validate_on_submit():

        job.title = form.title.data
        job.company = form.company.data
        job.location = form.location.data
        job.job_type = form.job_type.data
        job.category = form.category.data
        job.salary = form.salary.data
        job.description = form.description.data

        db.session.commit()

        flash(
            "Job updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "job.job_details",
                job_id=job.id
            )
        )

    return render_template(
        "job/edit.html",
        form=form,
        job=job
    )


# ==========================================
# DELETE JOB
# ==========================================

@job.route(
    "/jobs/<int:job_id>/delete",
    methods=["POST"]
)
def delete_job(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    db.session.delete(job)
    db.session.commit()

    flash(
        "Job deleted successfully!",
        "success"
    )

    return redirect(
        url_for(
            "job.list_jobs"
        )
    )