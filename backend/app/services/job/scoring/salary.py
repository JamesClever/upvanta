def salary_score(job):
    """
    Salary score between 0.0 and 1.0
    """

    salary = (
        job.get("salary")
        or job.get("salary_max")
        or job.get("salary_min")
    )

    if salary is None:
        return 0.0, "Salary not provided"

    try:

        salary = float(salary)

    except Exception:

        return 0.0, "Invalid salary"

    if salary >= 200000:
        return 1.0, "Excellent salary"

    if salary >= 150000:
        return 0.8, "High salary"

    if salary >= 100000:
        return 0.6, "Good salary"

    if salary >= 70000:
        return 0.4, "Average salary"

    return 0.2, "Entry salary"