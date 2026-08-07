from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ScholarshipForm(FlaskForm):

    title = StringField(
        "Scholarship Title",
        validators=[DataRequired()]
    )

    organization = StringField(
        "Organization",
        validators=[DataRequired()]
    )

    country = StringField("Country")

    level = StringField("Study Level")

    deadline = StringField("Deadline")

    amount = StringField("Amount")

    description = TextAreaField("Description")

    submit = SubmitField("Save Scholarship")