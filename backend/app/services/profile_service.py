def calculate_profile_completion(user):
    completed = 0

    fields = [
        user.full_name,
        user.email,
        user.profile_picture,
        user.bio,
        user.location,
        user.skills,
        user.education,
        user.experience
    ]

    for field in fields:
        if field:
            completed += 1

    return round((completed / len(fields)) * 100)