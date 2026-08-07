"""
Converts an internal ranking score into
a user-friendly match percentage.
"""


def calculate_match_percentage(score):

    if score <= 0:
        return 0

    MAX_SCORE = 180

    percentage = int(
        (score / MAX_SCORE) * 100
    )

    return min(100, percentage)