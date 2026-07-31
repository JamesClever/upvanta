from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.models.course import Course
from app.forms.course_form import CourseForm
from app.extensions import db

from .services import search_courses


courses = Blueprint(
    "courses",
    __name__
)


class ExternalCourse:

    def __init__(self, data):

        self.id = None
        self.title = data.get("title", "")
        self.platform = data.get("platform", "Web")
        self.category = data.get("category", "Online Course")
        self.level = data.get("level", "Various")
        self.duration = data.get("duration", "Online")
        self.description = data.get("description", "")
        self.url = data.get("url", "")
        self.external = True



@courses.route("/courses")
def list_courses():

    search = request.args.get(
        "search",
        ""
    ).strip()


    # ===============================
    # LOCAL DATABASE COURSES
    # ===============================

    local_query = Course.query


    if search:

        local_query = local_query.filter(
            Course.title.ilike(
                f"%{search}%"
            )
        )


    local_courses = (
        local_query
        .order_by(
            Course.id.desc()
        )
        .all()
    )



    # ===============================
    # GLOBAL WEB COURSES
    # ===============================

    web_courses = []


    if search:

        web_results = search_courses(
            search
        )

        web_courses = [
            ExternalCourse(course)
            for course in web_results
        ]



    # ===============================
    # COMBINE RESULTS
    # LOCAL FIRST, WEB SECOND
    # ===============================

    combined_courses = (
        local_courses
        +
        web_courses
    )



    class CourseResults:

        def __init__(self, items):

            self.items = items
            self.pages = 1
            self.page = 1
            self.has_prev = False
            self.has_next = False
            self.prev_num = None
            self.next_num = None



    courses_result = CourseResults(
        combined_courses
    )
        
    

    return render_template(
        "courses/courses.html",
        courses=courses_result,
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
            url_for(
                "courses.list_courses"
            )
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