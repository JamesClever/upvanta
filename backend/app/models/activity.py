from datetime import datetime

from app.extensions import db


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Which module generated this activity
    module = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    # Emoji shown on dashboard
    icon = db.Column(
        db.String(10),
        nullable=False
    )

    # Activity title
    # Example:
    # Resume Updated
    # Profile Picture Updated
    title = db.Column(
        db.String(200),
        nullable=False
    )

    # Page to open when clicked
    url = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "activities",
            lazy=True,
            order_by="Activity.created_at.desc()"
        )
    )

    def __repr__(self):
        return (
            f"<Activity {self.user_id} : "
            f"{self.title}>"
        )