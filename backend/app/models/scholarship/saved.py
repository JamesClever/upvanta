from datetime import datetime

from app.extensions import db



class SavedScholarship(db.Model):

    __tablename__ = "saved_scholarships"


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


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    scholarship = db.relationship(
        "Scholarship",
        backref="saved_by_users"
    )


    def __repr__(self):

        return f"<SavedScholarship {self.id}>"