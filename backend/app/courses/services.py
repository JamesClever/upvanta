from ddgs import DDGS
from urllib.parse import urlparse


COURSE_SITES = [
    "coursera.org",
    "udemy.com",
    "edx.org",
    "freecodecamp.org",
    "youtube.com",
    "learn.microsoft.com",
    "developer.mozilla.org",
    "aws.amazon.com",
    "codecademy.com",
    "cs50.harvard.edu",
    "w3schools.com",
    "programiz.com",
    "realpython.com",
    "kaggle.com",
    "datacamp.com",
    "pluralsight.com",
    "linkedin.com",
    "skillshare.com",
    "khanacademy.org",
    "futurecoder.io",
]


def get_platform(url, title):

    domain = urlparse(url).netloc.lower()

    platforms = {

        "coursera.org": "Coursera",
        "udemy.com": "Udemy",
        "edx.org": "edX",
        "freecodecamp.org": "freeCodeCamp",
        "youtube.com": "YouTube",

        "learn.microsoft.com": "Microsoft Learn",
        "developer.mozilla.org": "MDN Web Docs",
        "aws.amazon.com": "AWS Training",

        "codecademy.com": "Codecademy",
        "cs50.harvard.edu": "Harvard CS50",

        "w3schools.com": "W3Schools",
        "programiz.com": "Programiz",
        "realpython.com": "Real Python",

        "kaggle.com": "Kaggle",
        "datacamp.com": "DataCamp",
        "pluralsight.com": "Pluralsight",

        "linkedin.com": "LinkedIn Learning",
        "skillshare.com": "Skillshare",

        "khanacademy.org": "Khan Academy",
        "futurecoder.io": "FutureCoder",

        "learnpython.org": "LearnPython.org",

        "google.com": "Google Developers",
        "developers.google.com": "Google Developers",
        "codelabs.developers.google.com": "Google Codelabs",

        "python.org": "Python.org",

        "opencpython.org": "OpenPython",
        "geeksforgeeks.org": "GeeksforGeeks",
        "alison.com": "Alison",
        "python-course.eu": "Python Course EU",
        "python.org": "Python.org",
        "pythoninstitute.org": "Python Institute",
        "python.org": "Python.org",

    }


    for site, name in platforms.items():

        if site in domain:
            return name


    # fallback: extract platform from domain
    
    clean_domain = domain.replace("www.", "")

    platform_name = clean_domain.split(".")[0]


    invalid_platforms = [
        "market",
        "course",
        "courses",
        "learn",
        "training",
        "tutorial"
    ]


    if platform_name.lower() in invalid_platforms:
        return "Online Learning"


    return platform_name.replace("-", " ").title() 


def detect_category(text):

    text = text.lower()


    # ===============================
    # PROGRAMMING & SOFTWARE
    # ===============================

    if any(word in text for word in [
        "python",
        "javascript",
        "java",
        "coding",
        "programming",
        "software",
        "developer",
        "web development",
        "html",
        "css",
        "react",
        "node.js",
        "flask",
        "django"
    ]):

        return "Programming & Software"


    # ===============================
    # DATA SCIENCE & AI
    # ===============================

    if any(word in text for word in [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "data science",
        "analytics",
        "neural network",
        "tensorflow",
        "pytorch"
    ]):

        return "Data Science & AI"



    # ===============================
    # CLOUD & IT
    # ===============================

    if any(word in text for word in [
        "aws",
        "cloud",
        "devops",
        "network",
        "security",
        "cybersecurity",
        "azure",
        "linux"
    ]):

        return "Cloud & IT"



    # ===============================
    # BUSINESS & MARKETING
    # ===============================

    if any(word in text for word in [
        "business",
        "marketing",
        "entrepreneur",
        "sales",
        "finance",
        "management"
    ]):

        return "Business & Marketing"



    return "Professional Development"



def detect_level(text):

    text = text.lower()


    # ===============================
    # BEGINNER
    # ===============================

    if any(word in text for word in [
        "beginner",
        "for beginners",
        "introduction",
        "intro",
        "getting started",
        "basics",
        "basic",
        "fundamentals",
        "from scratch",
        "learn python"
    ]):

        return "Beginner"



    # ===============================
    # ADVANCED
    # ===============================

    if any(word in text for word in [
        "advanced",
        "expert",
        "masterclass",
        "deep dive",
        "professional level"
    ]):

        return "Advanced"



    # ===============================
    # DEFAULT
    # ===============================

    return "Intermediate"



def search_courses(query, max_results=15):

    search_query = (
        f"{query} "
        "beginner course "
        "learning tutorial "
        "training "
    )


    results = []


    with DDGS() as ddgs:


        search_results = list(
            ddgs.text(
                search_query,
                max_results=max_results
            )
        )


        for item in search_results:


            url = item.get(
                "href",
                ""
            )


            title = item.get(
                "title",
                ""
            )


            description = item.get(
                "body",
                ""
            )


            text = (
                title
                + " "
                + description
            ).lower()

            course_keywords = [

                "course",
                "tutorial",
                "learn",
                "training",
                "class",
                "lesson",
                "certification"

            ]


            if not any(
                word in text
                for word in course_keywords
            ):

                continue

            if query.lower() not in text:

                continue



            # Remove only clearly unrelated results

            blocked_words = [

                "wikipedia",
                "download",
                "installer",
                "github",
                "compiler",
                "documentation",
                "docs",
                "reference",
                "api",
                "news",
                "blog",
                "article",
                "forum",
                "community",
                "support",
                "certificate offer",
                "jobs"

            ]



            if any(
                word in text
                for word in blocked_words
            ):

                continue


            existing_titles = [
                course["title"].lower()
                for course in results
            ]


            if title.lower() in existing_titles:
                continue



            results.append(
                {

                    "title": title,


                    "platform": get_platform(
                        url,
                        title
                    ),


                    "category": detect_category(
                        text
                    ),


                    "level": detect_level(
                        text
                    ),


                    "duration": "Online",


                    "description": description,


                    "url": url,


                    "external": True

                }
            )



    # Rank actual courses higher

    priority_words = [
        "course",
        "tutorial",
        "certification",
        "training",
        "learn"
    ]


    def score(course):

        text = (
            course["title"] +
            " " +
            course["description"]
        ).lower()


        points = 0


        for word in priority_words:

            if word in text:

                points += 1


        if course["platform"] in [
            "Coursera",
            "Udemy",
            "edX",
            "Codecademy",
            "freeCodeCamp",
            "Harvard CS50"
        ]:

            points += 3


        return points



    results.sort(
        key=lambda x: (

            x["platform"] == "Online Learning",

            x["level"] != "Beginner"

        )
    )


    return results[:15]