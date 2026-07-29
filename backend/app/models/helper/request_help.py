from datetime import datetime

from app.extensions import db


# Help request status constants
REQUEST_PENDING = "pending"
REQUEST_ACCEPTED = "accepted"
REQUEST_DECLINED = "declined"
REQUEST_CANCELLED = "cancelled"
REQUEST_COMPLETED = "completed"


class HelpRequest(db.Model):

    __tablename__ = "help_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    requester_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    helper_id = db.Column(
        db.Integer,
        db.ForeignKey("helper.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(150),
        nullable=False
    )

    preferred_date = db.Column(
        db.Date
    )

    preferred_time = db.Column(
        db.Time
    )

    budget = db.Column(
        db.Float
    )

    status = db.Column(
        db.String(30),
        default=REQUEST_PENDING,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    requester = db.relationship(
        "User",
        foreign_keys=[requester_id]
    )

    helper = db.relationship(
        "Helper",
        foreign_keys=[helper_id]
    )

    def __repr__(self):
        return f"<HelpRequest {self.title}>"