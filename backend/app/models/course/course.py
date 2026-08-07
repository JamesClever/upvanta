from app.extensions import db
from datetime import datetime


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    platform = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    level = db.Column(
        db.String(100)
    )

    duration = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    def __repr__(self):
        return f"<Course {self.title}>"