from app.extensions import db
from datetime import datetime


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    company = db.Column(
        db.String(150),
        nullable=False
    )

    location = db.Column(
        db.String(150)
    )

    job_type = db.Column(
        db.String(50)
    )

    category = db.Column(
        db.String(100)
    )

    salary = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
        "JobApplication",
        backref="job",
        lazy=True,
        cascade="all, delete-orphan"
    )


    def __repr__(self):

        return f"<Job {self.title}>"
    