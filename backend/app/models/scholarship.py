from app.extensions import db
from datetime import datetime


class Scholarship(db.Model):

    __tablename__ = "scholarships"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    organization = db.Column(db.String(150), nullable=False)

    country = db.Column(db.String(100))

    level = db.Column(db.String(100))

    deadline = db.Column(db.String(100))

    amount = db.Column(db.String(100))

    description = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Scholarship {self.title}>"