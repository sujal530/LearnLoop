"""
models/user.py

User model for LearnLoop AI
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int = None

    name: str = ""
    email: str = ""
    password: str = ""

    skill_level: str = "Beginner"

    study_hours_per_day: int = 2

    streak: int = 0

    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # -----------------------------
    # Update Skill Level
    # -----------------------------
    def update_skill_level(self, level):
        self.skill_level = level

    # -----------------------------
    # Update Study Hours
    # -----------------------------
    def update_study_hours(self, hours):

        if hours > 0:
            self.study_hours_per_day = hours

    # -----------------------------
    # Increase Streak
    # -----------------------------
    def increase_streak(self):
        self.streak += 1

    # -----------------------------
    # Reset Streak
    # -----------------------------
    def reset_streak(self):
        self.streak = 0

    # -----------------------------
    # Convert Object to Dictionary
    # -----------------------------
    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "skill_level": self.skill_level,
            "study_hours_per_day": self.study_hours_per_day,
            "streak": self.streak,
            "created_at": self.created_at
        }

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):
        return f"{self.name} ({self.email})"
    