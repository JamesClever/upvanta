from datetime import datetime

from app.extensions import db


class ChatMessage(db.Model):

    __tablename__ = "chat_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    conversation = db.relationship(
        "Conversation",
        back_populates="messages"
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "chat_messages",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )