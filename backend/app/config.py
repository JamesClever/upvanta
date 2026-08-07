import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


class Config:

    # Flask security
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "change-this-in-production"
    )


    # Database
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(
            BASE_DIR,
            "upvanta.db"
        )
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Forms security
    WTF_CSRF_ENABLED = True


    # OpenAI API
    OPENAI_API_KEY = os.environ.get(
        "OPENAI_API_KEY"
    )

    # RapidAPI Job Search
    RAPIDAPI_KEY = os.environ.get(
        "RAPIDAPI_KEY"
    )