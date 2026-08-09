import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "careerpathindia_super_secret_key"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///careerpathindia.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    TEMPLATES_AUTO_RELOAD = True