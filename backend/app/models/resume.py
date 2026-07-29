from app.extensions import db
from datetime import datetime


class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(50)
    )

    location = db.Column(
        db.String(150)
    )

    education = db.Column(
        db.Text
    )

    experience = db.Column(
        db.Text
    )

    skills = db.Column(
        db.Text
    )

    summary = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Resume {self.full_name}>"