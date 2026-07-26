"""
helpers.py
Common helper functions for LearnLoop AI
"""

from datetime import datetime


# ------------------------------------
# Calculate Completion Percentage
# ------------------------------------
def calculate_completion(completed, total):
    """
    Returns completion percentage.
    """

    if total == 0:
        return 0

    return round((completed / total) * 100)


# ------------------------------------
# Format Date
# ------------------------------------
def format_date(date_string):
    """
    Converts YYYY-MM-DD into
    DD Month YYYY
    """

    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date.strftime("%d %B %Y")
    except:
        return date_string


# ------------------------------------
# Current Date
# ------------------------------------
def today():
    return datetime.now().strftime("%Y-%m-%d")


# ------------------------------------
# Greeting
# ------------------------------------
def greeting():

    hour = datetime.now().hour

    if hour < 12:
        return "Good Morning"

    elif hour < 17:
        return "Good Afternoon"

    return "Good Evening"


# ------------------------------------
# Study Level
# ------------------------------------
def learning_level(score):

    if score >= 90:
        return "Master"

    elif score >= 75:
        return "Advanced"

    elif score >= 60:
        return "Intermediate"

    elif score >= 40:
        return "Beginner"

    return "Starter"


# ------------------------------------
# Progress Color
# ------------------------------------
def progress_color(percent):

    if percent >= 80:
        return "success"

    elif percent >= 60:
        return "primary"

    elif percent >= 40:
        return "warning"

    return "danger"


# ------------------------------------
# Estimate Remaining Days
# ------------------------------------
def remaining_days(deadline):

    try:

        end = datetime.strptime(deadline, "%Y-%m-%d")

        remaining = (end - datetime.now()).days

        if remaining < 0:
            return 0

        return remaining

    except:
        return 0


# ------------------------------------
# Learning DNA Score
# ------------------------------------
def dna_score(consistency,
              confidence,
              understanding,
              quiz,
              study):

    score = (
        consistency +
        confidence +
        understanding +
        quiz +
        study
    ) / 5

    return round(score)


# ------------------------------------
# Streak Badge
# ------------------------------------
def streak_badge(days):

    if days >= 100:
        return "🏆 Legend"

    elif days >= 50:
        return "🔥 Expert"

    elif days >= 30:
        return "⭐ Pro"

    elif days >= 7:
        return "💪 Consistent"

    return "🌱 Beginner"
