from app.models.resume import Resume


def review_resume(resume):

    if resume is None:

        return {
            "overall_score": 0,
            "ats_score": 0,
            "grammar_score": 0,
            "strengths": [],
            "weaknesses": [
                "No resume has been created yet."
            ],
            "recommendations": [
                "Create your resume to receive AI feedback."
            ]
        }

    score = 0

    strengths = []

    weaknesses = []

    recommendations = []

    # ==========================================
    # PERSONAL DETAILS
    # ==========================================

    if resume.full_name:
        score += 5
    else:
        weaknesses.append("Missing full name.")

    if resume.email:
        score += 5
    else:
        weaknesses.append("Missing email address.")

    if resume.phone:
        score += 5
    else:
        recommendations.append("Add a phone number.")

    if resume.location:
        score += 5
    else:
        recommendations.append("Add your location.")

    # ==========================================
    # SUMMARY
    # ==========================================

    if resume.summary and len(resume.summary) > 80:

        score += 20

        strengths.append(
            "Professional summary looks good."
        )

    else:

        weaknesses.append(
            "Professional summary is too short."
        )

        recommendations.append(
            "Write a strong summary explaining your experience and career goals."
        )

    # ==========================================
    # EXPERIENCE
    # ==========================================

    if resume.experience:

        score += 20

        strengths.append(
            "Work experience included."
        )

        if len(resume.experience) < 120:

            recommendations.append(
                "Describe achievements instead of only responsibilities."
            )

    else:

        weaknesses.append(
            "No work experience added."
        )

    # ==========================================
    # EDUCATION
    # ==========================================

    if resume.education:

        score += 15

    else:

        recommendations.append(
            "Add your education."
        )

    # ==========================================
    # SKILLS
    # ==========================================

    if resume.skills:

        score += 20

        strengths.append(
            "Skills section completed."
        )

    else:

        weaknesses.append(
            "Skills section is empty."
        )

    # ==========================================
    # ATS SCORE
    # ==========================================

    ats_score = min(score, 100)

    # ==========================================
    # GRAMMAR SCORE
    # ==========================================

    grammar_score = 90

    # Placeholder until AI checks grammar

    # ==========================================
    # FINAL RECOMMENDATION
    # ==========================================

    if score >= 85:

        recommendations.append(
            "Your resume is in excellent shape."
        )

    elif score >= 70:

        recommendations.append(
            "Your resume is good but can be strengthened with more measurable achievements."
        )

    else:

        recommendations.append(
            "Complete more sections to improve your resume."
        )

    return {

        "overall_score": min(score, 100),

        "ats_score": ats_score,

        "grammar_score": grammar_score,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations

    }