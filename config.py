import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Secret key
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "mpath_career_counselling_default_secret_key_2026"
    )

    # Database configuration (supports PostgreSQL and SQLite)
    _db_url = os.environ.get("DATABASE_URL")
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url or (
        "sqlite:///" + os.path.join(BASE_DIR, "careerpathindia.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload limit (5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Environment-driven debug & reload
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1")
    TEMPLATES_AUTO_RELOAD = DEBUG