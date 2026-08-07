from datetime import datetime

from app.extensions import db


class UserMemory(db.Model):

    __tablename__ = "user_memories"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    memory_key = db.Column(
        db.String(100),
        nullable=False
    )


    memory_value = db.Column(
        db.Text,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )