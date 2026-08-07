from datetime import datetime

from app.extensions import db



class ScholarshipApplication(db.Model):

    __tablename__ = "scholarship_applications"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarships.id"),
        nullable=False
    )


    status = db.Column(
        db.String(50),
        default="Submitted"
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    scholarship = db.relationship(
        "Scholarship",
        backref="applications"
    )


    def __repr__(self):

        return f"<ScholarshipApplication {self.id}>"