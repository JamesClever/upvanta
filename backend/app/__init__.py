from flask import Flask

from .config import Config
from .extensions import db, login_manager, migrate, bcrypt

from .dashboard.main import main
from .dashboard.auth import auth
from .dashboard.routes import dashboard
from .dashboard.profile import profile

from .assist.routes import assist
from .job.routes import job
from .course.routes import course
from .scholarship.routes import scholarship
from .mentorship.routes import mentorship
from .resume.routes import resume
from .helper.routes import helper
from .ai.routes import ai

from .models import User


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Core
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(profile)

    # Features
    app.register_blueprint(assist)
    app.register_blueprint(job)
    app.register_blueprint(course)
    app.register_blueprint(scholarship)
    app.register_blueprint(mentorship)
    app.register_blueprint(resume)
    app.register_blueprint(helper)
    app.register_blueprint(ai)

    return app