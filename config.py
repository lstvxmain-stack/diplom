import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'data', 'cultural.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # Flask-Admin
    FLASK_ADMIN_SWATCH = "cosmo"

    # Upload folder for images
    UPLOAD_FOLDER = os.path.join(basedir, "project", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
