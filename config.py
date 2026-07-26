import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # -------------------------------
    # Flask Configuration
    # -------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "learnloopai_secret_key")

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
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

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
    # Uploads
    # -------------------------------
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    # -------------------------------
    # Session
    # -------------------------------
    SESSION_TYPE = "filesystem"

    # -------------------------------
    # Debug
    # -------------------------------
    DEBUG = True