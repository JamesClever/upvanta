from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user

from app.forms.register_form import RegisterForm
from app.models.user import User
from app.extensions import db, bcrypt


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        # Check if email already exists
        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()


        if existing_user:

            flash(
                "Email already registered. Please login.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )


        # Hash password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")


        # Create new user
        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=hashed_password
        )


        db.session.add(user)
        db.session.commit()


        flash(
            "Account created successfully!",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "auth/register.html",
        form=form
    )



@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")


        user = User.query.filter_by(
            email=email
        ).first()


        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            login_user(user)


            flash(
                "Login successful!",
                "success"
            )


            return redirect(
                url_for("dashboard.index")
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "auth/login.html"
    )



@auth.route("/logout")
def logout():

    logout_user()


    flash(
        "Logged out successfully.",
        "success"
    )


    return redirect(
        url_for("main.home")
    )