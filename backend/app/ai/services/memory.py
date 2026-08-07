from app.extensions import db
from app.models.ai.ai_memory import UserMemory


def extract_memories(user_id, message):
    """
    Extract simple long-term memories from user messages.
    """

    message_lower = message.lower()

    memories_to_save = []


    # Career interests

    if "i want to become" in message_lower:

        value = message.split(
            "i want to become",
            1
        )[1].strip()

        memories_to_save.append(
            (
                "career_goal",
                value
            )
        )


    # Skills

    if "my skills are" in message_lower:

        value = message.split(
            "my skills are",
            1
        )[1].strip()

        memories_to_save.append(
            (
                "skills",
                value
            )
        )


    # Education

    if "i studied" in message_lower:

        value = message.split(
            "i studied",
            1
        )[1].strip()

        memories_to_save.append(
            (
                "education",
                value
            )
        )


    for key, value in memories_to_save:

        existing = UserMemory.query.filter_by(
            user_id=user_id,
            memory_key=key
        ).first()


        if existing:

            existing.memory_value = value

        else:

            memory = UserMemory(
                user_id=user_id,
                memory_key=key,
                memory_value=value
            )

            db.session.add(memory)


    db.session.commit()



def get_user_memories(user_id):

    """
    Retrieve saved user memories.
    """

    return (
        UserMemory.query
        .filter_by(user_id=user_id)
        .order_by(UserMemory.created_at.desc())
        .all()
    )