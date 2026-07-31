from flask import Blueprint, render_template, abort
from flask import request, redirect, url_for, flash

from flask_login import login_required, current_user

from app.models.job import Job
from app.models.job_application import JobApplication

from app.forms.job_form import JobForm
from app.extensions import db

from app.services.job_application_service import apply_for_job

jobs = Blueprint("jobs", __name__)

@jobs.route("/jobs")
def list_jobs():

    search = request.args.get("search", "")

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = Job.query

    if search:

        query = query.filter(
            Job.title.contains(search)
        )

    jobs = query.order_by(
        Job.id.desc()
    ).paginate(
        page=page,
        per_page=12
    )

    return render_template(
        "jobs/jobs.html",
        jobs=jobs,
        search=search
    )

@jobs.route("/jobs/<int:job_id>")
def job_details(job_id):

    job = Job.query.get_or_404(job_id)

    return render_template(
        "jobs/job_details.html",
        job=job
    )


@jobs.route("/jobs/<int:job_id>/apply", methods=["POST"])
@login_required
def apply_job(job_id):

    job = Job.query.get_or_404(job_id)

    application, created = apply_for_job(
        current_user,
        job
    )

    if created:

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
            "jobs.job_details",
            job_id=job.id
        )
    )


@jobs.route("/jobs/add", methods=["GET", "POST"])
def add_job():

    form = JobForm()

    print("REQUEST METHOD:", request.method)
    print("FORM DATA:", request.form)

    if form.validate_on_submit():

        print("FORM VALIDATED!")

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

        flash("Job added successfully!", "success")

        return redirect(url_for("jobs.list_jobs"))

    print("FORM ERRORS:", form.errors)

    return render_template(
        "jobs/add_job.html",
        form=form
    )

@jobs.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id):

    job = Job.query.get_or_404(job_id)

    form = JobForm(obj=job)

    if form.validate_on_submit():

        job.title = form.title.data
        job.company = form.company.data
        job.location = form.location.data
        job.job_type = form.job_type.data
        job.category = form.category.data
        job.salary = form.salary.data
        job.description = form.description.data

        db.session.commit()

        flash("Job updated successfully!", "success")

        return redirect(url_for("jobs.job_details", job_id=job.id))

    return render_template(
        "jobs/edit_job.html",
        form=form,
        job=job
    )
    
@jobs.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):

    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully!", "success")

    return redirect(url_for("jobs.list_jobs"))