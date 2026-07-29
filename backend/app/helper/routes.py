from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_required,
    current_user,
)

from app.extensions import db

from app.models.helper import (
    Helper,
    HelpRequest,
    REQUEST_ACCEPTED,
    REQUEST_DECLINED,
    REQUEST_CANCELLED,
    REQUEST_COMPLETED,
)

from . import helper


# =====================================================
# Become an Upvanta Helper
# =====================================================

@helper.route("/become-helper", methods=["GET", "POST"])
@login_required
def become_helper():

    helper_profile = Helper.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        if helper_profile is None:
            helper_profile = Helper(
                user_id=current_user.id
            )
            db.session.add(helper_profile)

        helper_profile.location = request.form.get(
            "location",
            ""
        ).strip()

        helper_profile.services = request.form.get(
            "services",
            ""
        ).strip()

        helper_profile.availability = request.form.get(
            "availability",
            "Available"
        )

        helper_profile.about = request.form.get(
            "about",
            ""
        ).strip()

        hourly_rate = request.form.get(
            "hourly_rate",
            ""
        ).strip()

        try:
            helper_profile.hourly_rate = (
                float(hourly_rate)
                if hourly_rate
                else 0
            )
        except ValueError:

            flash(
                "Hourly rate must be a valid number.",
                "danger"
            )

            return render_template(
                "helper/become_helper.html",
                user=current_user
            )

        current_user.is_helper = True

        db.session.commit()

        flash(
            "Congratulations! You are now an Upvanta Helper.",
            "success"
        )

        return redirect(
            url_for("profile.index")
        )

    return render_template(
        "helper/become_helper.html",
        user=current_user
    )


# =====================================================
# Request Help
# =====================================================

@helper.route("/request-help/<int:helper_id>", methods=["GET", "POST"])
@login_required
def request_help(helper_id):

    helper_profile = Helper.query.get_or_404(helper_id)

    if request.method == "POST":

        preferred_date = request.form.get("preferred_date")
        preferred_time = request.form.get("preferred_time")

        try:

            preferred_date = (
                datetime.strptime(
                    preferred_date,
                    "%Y-%m-%d"
                ).date()
                if preferred_date
                else None
            )

            preferred_time = (
                datetime.strptime(
                    preferred_time,
                    "%H:%M"
                ).time()
                if preferred_time
                else None
            )

        except ValueError:

            flash(
                "Please enter a valid date and time.",
                "danger"
            )

            return render_template(
                "helper/request_help.html",
                helper=helper_profile
            )

        budget = request.form.get(
            "budget",
            ""
        ).strip()

        try:
            budget = float(budget) if budget else 0
        except ValueError:

            flash(
                "Budget must be a valid number.",
                "danger"
            )

            return render_template(
                "helper/request_help.html",
                helper=helper_profile
            )

        help_request = HelpRequest(
            requester_id=current_user.id,
            helper_id=helper_profile.id,
            title=request.form.get("title", "").strip(),
            description=request.form.get(
                "description",
                ""
            ).strip(),
            location=request.form.get(
                "location",
                ""
            ).strip(),
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            budget=budget,
        )

        db.session.add(help_request)
        db.session.commit()

        flash(
            "Your request has been sent successfully!",
            "success"
        )

        return redirect(
            url_for("assist.index")
        )

    return render_template(
        "helper/request_help.html",
        helper=helper_profile
    )

# =====================================================
# View Help Request Details
# =====================================================

@helper.route("/request/<int:request_id>")
@login_required
def request_details(request_id):

    help_request = HelpRequest.query.get_or_404(
        request_id
    )

    return render_template(
        "helper/request_details.html",
        help_request=help_request
    )

# =====================================================
# Accept Help Request
# =====================================================

@helper.route("/request/<int:request_id>/accept")
@login_required
def accept_request(request_id):

    help_request = HelpRequest.query.get_or_404(
        request_id
    )

    if help_request.helper.user_id != current_user.id:
        flash(
            "You cannot accept this request.",
            "danger"
        )
        return redirect(
            url_for("assist.index")
        )

    help_request.status = REQUEST_ACCEPTED

    db.session.commit()

    flash(
        "Request accepted successfully.",
        "success"
    )

    return redirect(
        url_for("assist.index")
    )

# =====================================================
# Decline Help Request
# =====================================================

@helper.route("/request/<int:request_id>/decline")
@login_required
def decline_request(request_id):

    help_request = HelpRequest.query.get_or_404(
        request_id
    )

    if help_request.helper.user_id != current_user.id:
        flash(
            "You cannot decline this request.",
            "danger"
        )
        return redirect(
            url_for("assist.index")
        )

    help_request.status = REQUEST_DECLINED

    db.session.commit()

    flash(
        "Request declined.",
        "info"
    )

    return redirect(
        url_for("assist.index")
    )

# =====================================================
# Cancel Help Request
# =====================================================

@helper.route("/request/<int:request_id>/cancel")
@login_required
def cancel_request(request_id):

    help_request = HelpRequest.query.get_or_404(
        request_id
    )

    if help_request.requester_id != current_user.id:
        flash(
            "You cannot cancel this request.",
            "danger"
        )

        return redirect(
            url_for("assist.index")
        )

    help_request.status = REQUEST_CANCELLED

    db.session.commit()

    flash(
        "Request cancelled.",
        "warning"
    )

    return redirect(
        url_for("assist.index")
    )

# =====================================================
# Complete Help Request
# =====================================================

@helper.route("/request/<int:request_id>/complete")
@login_required
def complete_request(request_id):

    help_request = HelpRequest.query.get_or_404(
        request_id
    )

    if help_request.helper.user_id != current_user.id:
        flash(
            "You cannot complete this request.",
            "danger"
        )

        return redirect(
            url_for("assist.index")
        )

    help_request.status = REQUEST_COMPLETED

    db.session.commit()

    flash(
        "Request marked as completed.",
        "success"
    )

    return redirect(
        url_for("assist.index")
    )

    