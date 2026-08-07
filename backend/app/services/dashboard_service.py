from app.services.activity.activity import get_recent_activities

# ==========================================
# DASHBOARD DATA
# ==========================================

def dashboard_data(user):
    """
    Returns all dashboard data.

    As the dashboard grows,
    this will become the single place
    for assembling everything the
    dashboard needs.
    """

    return {

        "recent_activities": get_recent_activities(user)

    }