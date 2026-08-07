from flask import Blueprint, render_template, redirect, url_for, flash, request

from flask_login import login_required, current_user

from app.models.resume.resume import Resume
from app.forms.resume.form import ResumeForm

from app.services.resume.reviewer import review_resume
from app.services.activity.activity import create_activity

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
            Resume.full_name.ilike(
                f"%{search}%"
            )
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



@resume.route(
    "/resume/add",
    methods=["GET", "POST"]
)
@login_required
def add_resume():


    user_resume = Resume.query.filter_by(
        user_id=current_user.id
    ).first()


    # ==========================================
    # LOAD FORM
    # ==========================================

    if request.method == "GET":

        if user_resume:

            form = ResumeForm(
                obj=user_resume
            )

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


        if user_resume is None:


            user_resume = Resume(
                user_id=current_user.id
            )

            db.session.add(
                user_resume
            )


        user_resume.full_name = (
            form.full_name.data
        )

        user_resume.email = (
            form.email.data
        )

        user_resume.phone = (
            form.phone.data
        )

        user_resume.location = (
            form.location.data
        )

        user_resume.education = (
            form.education.data
        )

        user_resume.experience = (
            form.experience.data
        )

        user_resume.skills = (
            form.skills.data
        )

        user_resume.summary = (
            form.summary.data
        )


        db.session.commit()



        # ==========================================
        # ACTIVITY ENGINE
        # ==========================================

        create_activity(
            current_user,
            icon="📄",
            title="Resume Updated",
            url=url_for(
                "resume.list_resumes"
            ),
            module="resume"
        )


        flash(
            "Resume saved successfully!",
            "success"
        )


        return redirect(
            url_for(
                "resume.list_resumes"
            )
        )


    return render_template(
        "resume/edit.html",
        form=form
    )



@resume.route("/resume/review")
@login_required
def review():


    user_resume = Resume.query.filter_by(
        user_id=current_user.id
    ).first()



    if user_resume is None:

        flash(
            "Create a resume before requesting a review.",
            "warning"
        )

        return redirect(
            url_for(
                "resume.add_resume"
            )
        )



    review_result = review_resume(
        user_resume
    )


    return render_template(
        "resume/review.html",
        resume=user_resume,
        review=review_result
    )