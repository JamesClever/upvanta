from ..companies import TOP_COMPANIES


def company_score(job):
    """
    Score company reputation.

    Returns:
        score (float): 0.0 - 1.0
        reason (str)
    """

    company = (job.get("company") or "").lower()

    if not company:
        return 0.0, "Unknown company"

    for company_name, bonus in TOP_COMPANIES.items():

        if company_name in company:

            normalized = min(bonus / 20, 1.0)

            return normalized, f"Top employer: {company_name.title()}"

    return 0.3, "Standard employer"