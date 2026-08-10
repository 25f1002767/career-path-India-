import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Secret key
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "careerpathindia_super_secret_key"
    )

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "careerpathindia.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload limit
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Auto reload templates during development
    TEMPLATES_AUTO_RELOAD = True