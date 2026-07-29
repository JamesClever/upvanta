from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):

    title = StringField(
        "Course Title",
        validators=[DataRequired()]
    )


    platform = StringField(
        "Platform",
        validators=[DataRequired()]
    )


    category = StringField(
        "Category"
    )


    level = StringField(
        "Level"
    )


    duration = StringField(
        "Duration"
    )


    description = TextAreaField(
        "Description"
    )


    submit = SubmitField(
        "Save Course"
    )