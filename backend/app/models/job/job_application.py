from datetime import datetime

from app.extensions import db


class JobApplication(db.Model):

    __tablename__ = "job_applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # Relationships
    # ==========================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    # ==========================================
    # Application Details
    # ==========================================

    status = db.Column(
        db.String(30),
        default="Applied"
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    interview_date = db.Column(
        db.DateTime
    )

    # ==========================================
    # Resume Used
    # ==========================================

    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resumes.id")
    )

    # ==========================================
    # Application Content
    # ==========================================

    cover_letter = db.Column(
        db.Text
    )

    notes = db.Column(
        db.Text
    )

    # ==========================================
    # Tracking
    # ==========================================

    source = db.Column(
        db.String(100),
        default="Upvanta"
    )

    ai_match_score = db.Column(
        db.Integer,
        default=0
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<JobApplication {self.user_id}-{self.job_id}>"