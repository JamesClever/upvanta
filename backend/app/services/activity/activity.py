from app.extensions import db
from app.models.activity import Activity


def create_activity(
    user,
    icon,
    title,
    url,
    module
):
    """
    Create and save a user activity.
    """

    activity = Activity(
        user_id=user.id,
        module=module,
        icon=icon,
        title=title,
        url=url
    )

    db.session.add(activity)
    db.session.commit()

    return activity


def get_recent_activities(
    user,
    limit=10
):
    """
    Get the most recent activities for a user.
    """

    return (
        Activity.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            Activity.created_at.desc()
        )
        .limit(limit)
        .all()
    )

def profile_snapshot(user):
    """
    Capture current profile information
    before an update.

    Used to compare profile changes.
    """

    return {

        "full_name": user.full_name,

        "bio": user.bio,

        "location": user.location,

        "skills": user.skills,

        "education": user.education,

        "experience": user.experience,

        "profile_picture": user.profile_picture,

    }