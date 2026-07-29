from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):

    title = StringField(
        "Job Title",
        validators=[DataRequired()]
    )

    company = StringField(
        "Company",
        validators=[DataRequired()]
    )

    location = StringField(
        "Location",
        validators=[DataRequired()]
    )

    job_type = StringField(
        "Job Type",
        validators=[DataRequired()]
    )

    category = StringField(
        "Category",
        validators=[DataRequired()]
    )

    salary = StringField(
        "Salary",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Job")