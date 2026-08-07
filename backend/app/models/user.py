from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversations = db.relationship(
        "Conversation",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Memories
    
    memories = db.relationship(
        "UserMemory",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Authentication

    full_name = db.Column(
        db.String(100),
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )

    profile_picture = db.Column(
        db.String(255),
        default="default_avatar.webp"
    )


    bio = db.Column(
        db.Text,
        default=""
    )


    location = db.Column(
        db.String(100),
        default=""
    )


    skills = db.Column(
        db.String(255),
        default=""
    )


    education = db.Column(
        db.String(255),
        default=""
    )


    experience = db.Column(
        db.Text,
        default=""
    )

    resumes = db.relationship(
        "Resume",
        backref="user",
        lazy=True
    )

    saved_scholarships = db.relationship(
        "SavedScholarship",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


    scholarship_applications = db.relationship(
        "ScholarshipApplication",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


    # Upvanta Assist

    is_helper = db.Column(
        db.Boolean,
        default=False
    )


    availability = db.Column(
        db.String(50),
        default="Not Available"
    )


    rating = db.Column(
        db.Float,
        default=0.0
    )


    completed_tasks = db.Column(
        db.Integer,
        default=0
    )


    def __repr__(self):
        return f"<User {self.email}>"