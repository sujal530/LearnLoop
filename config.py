import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # -------------------------------
    # Flask Configuration
    # -------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "learnloopai_secret_key_default_change_me")

    # -------------------------------
    # Project Paths
    # -------------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # -------------------------------
    # Database
    # -------------------------------
    DATABASE = os.path.join(BASE_DIR, "database", "database.db")

    # -------------------------------
    # Gemini AI
    # -------------------------------
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    # -------------------------------
    # Learning Settings
    # -------------------------------
    DEFAULT_STUDY_HOURS = 2
    DEFAULT_STREAK = 0
    DEFAULT_PROGRESS = 0

    # -------------------------------
    # Quiz
    # -------------------------------
    QUIZ_QUESTIONS = 10
    PASS_PERCENTAGE = 70

    # -------------------------------
    # Roadmap
    # -------------------------------
    MAX_WEEKS = 12
    DAILY_TASK_LIMIT = 5

    # -------------------------------
    # Learning DNA
    # -------------------------------
    DNA_FACTORS = [
        "Consistency",
        "Confidence",
        "Understanding",
        "Quiz Performance",
        "Study Hours",
    ]

    # -------------------------------
    # Uploads & File Handling
    # -------------------------------
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit file uploads to 16 MB

    # Ensure uploads folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # -------------------------------
    # Debug
    # -------------------------------
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")