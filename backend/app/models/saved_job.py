from app.extensions import db


saved_jobs = db.Table(

    "saved_jobs",

    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),

    db.Column(
        "job_id",
        db.Integer,
        db.ForeignKey("jobs.id"),
        primary_key=True
    )

)