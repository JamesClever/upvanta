from datetime import datetime
from app.extensions import db


class Mentorship(db.Model):
    __tablename__ = "mentorships"

    id = db.Column(db.Integer, primary_key=True)

    mentor = db.Column(db.String(150), nullable=False)

    expertise = db.Column(db.String(150), nullable=False)

    organization = db.Column(db.String(150))

    location = db.Column(db.String(100))

    availability = db.Column(db.String(100))

    description = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )