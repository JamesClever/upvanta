from .semantic import semantic_bonus
from .company_score import TOP_COMPANIES
from .recent import recent_bonus
from .personalization import personalization_bonus
from .resume_match import resume_match_score
from .match_percentage import calculate_match_percentage

def rank_jobs(jobs, query, user=None):

    query = query.lower()

    ranked = []

    for job in jobs:

        score = 0

        title = (job.get("title") or "").lower()

        description = (
            job.get("description") or ""
        ).lower()

        company = (
            job.get("company") or ""
        ).lower()

        location = (
            job.get("location") or ""
        ).lower()

        source = (
            job.get("source") or ""
        ).lower()

        # -------------------------
        # Title Match
        # -------------------------

        if query in title:
            score += 50

        # -------------------------
        # Description Match
        # -------------------------

        if query in description:
            score += 20

        # -------------------------
        # Company Match
        # -------------------------

        if query in company:
            score += 10

        # -------------------------
        # Location Match
        # -------------------------

        if query in location:
            score += 10

        # -------------------------
        # Remote bonus
        # -------------------------

        if "remote" in title:
            score += 15

        if "remote" in description:
            score += 15

        # -------------------------
        # Salary bonus
        # -------------------------

        salary = job.get("salary")

        if salary:

            try:

                salary = float(salary)

                if salary >= 150000:
                    score += 20

                elif salary >= 100000:
                    score += 15

                elif salary >= 70000:
                    score += 10

            except:

                pass

        # -------------------------
        # Trusted source bonus
        # -------------------------

        if source == "jsearch":
            score += 5

        elif source == "adzuna":
            score += 3

        company_name = company.lower()

        for company_key, bonus in TOP_COMPANIES.items():
            if company_key in company_name:
                score += bonus
                break

        # -------------------------
        # recent bonus
        # -------------------------

        score += recent_bonus(job)

        # -------------------------
        # Semantic Search Bonus
        # -------------------------

        score += semantic_bonus(
            job,
            query
        )

        # -------------------------
        # Personalized ranking
        # -------------------------

        score += personalization_bonus(
            job,
            user
        )

        score += resume_match_score(job, user)

        job["score"] = score

        job["match"] = calculate_match_percentage(
            score
        )

        ranked.append(job)

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked