from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import DataRequired, Email


class ResumeForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField("Phone Number")

    location = StringField("Location")

    education = TextAreaField("Education")

    experience = TextAreaField("Work Experience")

    skills = TextAreaField("Skills")

    summary = TextAreaField("Professional Summary")

    submit = SubmitField("Save Resume")