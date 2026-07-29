import re

from app.extensions import db
from app.models.ai_memory import UserMemory



def save_memory(user_id, key, value):
    """
    Save a user memory if it does not already exist.
    """

    existing = UserMemory.query.filter_by(
        user_id=user_id,
        memory_key=key,
        memory_value=value
    ).first()


    if existing:
        return


    memory = UserMemory(
        user_id=user_id,
        memory_key=key,
        memory_value=value
    )

    db.session.add(memory)
    db.session.commit()



def extract_memories(user_id, message):
    """
    Analyze user message and extract useful personal information.
    """

    text = message.strip()


    lower_text = text.lower()



    # -------------------------
    # EDUCATION
    # -------------------------

    education_patterns = [
        r"studying (.+?)(?: at| in|$)",
        r"study (.+?)(?: at| in|$)",
        r"learning (.+)"
    ]


    for pattern in education_patterns:

        match = re.search(pattern, text, re.I)

        if match:
            education = match.group(1).strip()

            save_memory(
                user_id,
                "education",
                education
            )

            break



    # -------------------------
    # INSTITUTION
    # -------------------------

    institution_patterns = [
        r"at ([A-Za-z0-9\-\s]+)",
        r"from ([A-Za-z0-9\-\s]+)"
    ]


    for pattern in institution_patterns:

        match = re.search(pattern, text, re.I)

        if match:

            institution = match.group(1).strip()


            save_memory(
                user_id,
                "institution",
                institution
            )

            break



    # -------------------------
    # CAREER GOAL
    # -------------------------

    career_patterns = [
        r"want to become (.+)",
        r"wanna become (.+)",
        r"my goal is to become (.+)",
        r"aim to become (.+)"
    ]


    for pattern in career_patterns:

        match = re.search(pattern, text, re.I)

        if match:

            goal = match.group(1).strip()


            save_memory(
                user_id,
                "career_goal",
                goal
            )

            break



    # -------------------------
    # SKILLS
    # -------------------------

    skills = [
        "python",
        "flask",
        "javascript",
        "node.js",
        "react",
        "sql",
        "html",
        "css",
        "django"
    ]


    found_skills = []


    for skill in skills:

        if skill.lower() in lower_text:
            found_skills.append(skill)



    if found_skills:

        save_memory(
            user_id,
            "skills",
            ", ".join(found_skills)
        )



    # -------------------------
    # JOB ROLE
    # -------------------------

    job_patterns = [
        r"work as a (.+)",
        r"i am a (.+)",
        r"my job is (.+)"
    ]


    for pattern in job_patterns:

        match = re.search(pattern, text, re.I)

        if match:

            role = match.group(1).strip()


            save_memory(
                user_id,
                "job_role",
                role
            )

            break



    return True



def get_user_memories(user_id):

    return UserMemory.query.filter_by(
        user_id=user_id
    ).all()