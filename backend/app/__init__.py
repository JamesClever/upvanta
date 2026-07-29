from flask import Flask

from .config import Config
from .extensions import db, login_manager, migrate, bcrypt

from .routes.main import main
from .routes.auth import auth
from .routes.dashboard import dashboard
from .routes.profile import profile
from .assist.routes import assist
from .scholarships.routes import scholarships
from .courses.routes import courses
from .resume.routes import resume
from .mentorships.routes import mentorships
from .helper import helper
from .ai import ai


from .models import User, Job, Scholarship, Helper

from .jobs.routes import jobs


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


    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(profile)
    app.register_blueprint(assist)
    app.register_blueprint(jobs)
    app.register_blueprint(scholarships)
    app.register_blueprint(courses)
    app.register_blueprint(resume)
    app.register_blueprint(mentorships)
    app.register_blueprint(helper)
    app.register_blueprint(ai)
    

    return app