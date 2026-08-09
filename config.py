import os

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(BASE_DIR, "careerpathindia.db")
)
class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "careerpathindia_super_secret_key"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    TEMPLATES_AUTO_RELOAD = True