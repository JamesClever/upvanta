from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.course import Course
from app.forms.course_form import CourseForm
from app.extensions import db


courses = Blueprint(
    "courses",
    __name__
)


@courses.route("/courses")
def list_courses():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = Course.query

    if search:
        query = query.filter(
            Course.title.ilike(f"%{search}%")
        )

    courses = query.order_by(
        Course.id.desc()
    ).paginate(
        page=page,
        per_page=12,
        error_out=False
    )

    return render_template(
        "courses/courses.html",
        courses=courses,
        search=search
    )



@courses.route("/courses/add", methods=["GET", "POST"])
def add_course():

    form = CourseForm()

    if form.validate_on_submit():

        course = Course(

            title=form.title.data,
            platform=form.platform.data,
            category=form.category.data,
            level=form.level.data,
            duration=form.duration.data,
            description=form.description.data
        )


        db.session.add(course)
        db.session.commit()


        flash(
            "Course added successfully!",
            "success"
        )


        return redirect(
            url_for("courses.list_courses")
        )


    return render_template(
        "courses/add_course.html",
        form=form
    )



@courses.route("/courses/<int:course_id>")
def course_details(course_id):

    course = Course.query.get_or_404(
        course_id
    )

    return render_template(
        "courses/details.html",
        course=course
    )