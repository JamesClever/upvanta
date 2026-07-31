from flask import Blueprint, render_template, redirect, url_for, flash, request

from flask_login import login_required, current_user
from app.models.resume import Resume
from app.forms.resume_form import ResumeForm
from app.services.ai_resume_review_service import review_resume
from app.extensions import db


resume = Blueprint(
    "resume",
    __name__
)


@resume.route("/resume")
@login_required
def list_resumes():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = Resume.query.filter_by(
        user_id=current_user.id
    )

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


    # ==========================================
    # AI REVIEW SCORES FOR RESUME CARDS
    # ==========================================

    resume_reviews = {}

    for item in resumes.items:

        resume_reviews[item.id] = review_resume(
            item
        )


    return render_template(
        "resume/resume.html",
        resumes=resumes,
        search=search,
        resume_reviews=resume_reviews
    )

@resume.route("/resume/add", methods=["GET", "POST"])
@login_required
def add_resume():

    resume = Resume.query.filter_by(
        user_id=current_user.id
    ).first()

    # ==========================================
    # GET REQUEST
    # ==========================================

    if request.method == "GET":

        if resume:

            form = ResumeForm(obj=resume)

        else:

            form = ResumeForm(
                data={
                    "full_name": current_user.full_name,
                    "email": current_user.email,
                    "location": current_user.location,
                    "education": current_user.education,
                    "experience": current_user.experience,
                    "skills": current_user.skills,
                }
            )

    else:

        form = ResumeForm()

    # ==========================================
    # SAVE RESUME
    # ==========================================

    if form.validate_on_submit():

        if resume is None:

            resume = Resume(
                user_id=current_user.id
            )

            db.session.add(resume)

        resume.full_name = form.full_name.data
        resume.email = form.email.data
        resume.phone = form.phone.data
        resume.location = form.location.data
        resume.education = form.education.data
        resume.experience = form.experience.data
        resume.skills = form.skills.data
        resume.summary = form.summary.data

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

@resume.route("/resume/review")
@login_required
def review():

    resume = Resume.query.filter_by(
        user_id=current_user.id
    ).first()


    review_result = review_resume(
        resume
    )


    return render_template(
        "resume/review.html",
        resume=resume,
        review=review_result
    )