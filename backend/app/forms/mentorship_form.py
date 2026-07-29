from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MentorshipForm(FlaskForm):

    mentor = StringField(
        "Mentor Name",
        validators=[DataRequired()]
    )

    expertise = StringField(
        "Expertise",
        validators=[DataRequired()]
    )

    organization = StringField("Organization")

    location = StringField("Location")

    availability = StringField("Availability")

    description = TextAreaField("Description")

    submit = SubmitField("Save Mentorship")