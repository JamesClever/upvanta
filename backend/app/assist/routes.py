from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.helper import (
    Helper,
    HelpRequest,
)

assist = Blueprint(
    "assist",
    __name__
)


@assist.route("/assist")
@login_required
def index():

    # All available helpers
    helpers = Helper.query.all()


    # Requests created by the logged-in user
    my_requests = (
        HelpRequest.query
        .filter_by(
            requester_id=current_user.id
        )
        .order_by(
            HelpRequest.created_at.desc()
        )
        .all()
    )


    # Requests received by the logged-in user
    # only if they are a helper
    incoming_requests = []

    if current_user.helper_profile:

        incoming_requests = (
            HelpRequest.query
            .filter_by(
                helper_id=current_user.helper_profile.id
            )
            .order_by(
                HelpRequest.created_at.desc()
            )
            .all()
        )


    return render_template(
        "assist/assist.html",
        helpers=helpers,
        my_requests=my_requests,
        incoming_requests=incoming_requests
    )


@assist.route("/assist/helper/<int:helper_id>")
@login_required
def helper_profile(helper_id):

    helper = Helper.query.get_or_404(helper_id)

    return render_template(
        "assist/helper_profile.html",
        helper=helper
    )