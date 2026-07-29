from app.extensions import db
from sqlalchemy.orm import backref


class Helper(db.Model):

    __tablename__ = "helper"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    location = db.Column(db.String(120))
    services = db.Column(db.Text)

    availability = db.Column(
        db.String(30),
        default="Available"
    )

    hourly_rate = db.Column(db.Float, default=0)

    verified = db.Column(
        db.Boolean,
        default=False
    )

    rating = db.Column(
        db.Float,
        default=5.0
    )

    jobs_completed = db.Column(
        db.Integer,
        default=0
    )

    about = db.Column(db.Text)

    user = db.relationship(
        "User",
        backref=backref(
            "helper_profile",
            uselist=False
        )
    )