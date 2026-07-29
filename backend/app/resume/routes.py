from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.resume import Resume
from app.forms.resume_form import ResumeForm
from app.extensions import db


resume = Blueprint(
    "resume",
    __name__
)


@resume.route("/resume")
def list_resumes():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = Resume.query

    if search:
        query = query.filter(
            Resume.full_name.ilike(f"%{search}%")
        )

    resumes = query.order_by(
        Resume.id.desc()
    ).paginate(
        page=page,
        per_page=12,
        error_out=False
    )

    return render_template(
        "resume/resume.html",
        resumes=resumes,
        search=search
    )

@resume.route("/resume/add", methods=["GET", "POST"])
def add_resume():

    form = ResumeForm()

    if form.validate_on_submit():

        new_resume = Resume(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            location=form.location.data,
            education=form.education.data,
            experience=form.experience.data,
            skills=form.skills.data,
            summary=form.summary.data
        )

        db.session.add(new_resume)
        db.session.commit()

        flash(
            "Resume saved successfully!",
            "success"
        )

        return redirect(
            url_for("resume.list_resumes")
        )

    return render_template(
        "resume/edit_resume.html",
        form=form
    )