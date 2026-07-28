"""
models/user.py

User model for LearnLoop AI
"""

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from config import Config


@dataclass
class User:
    id: int = None

    name: str = ""
    email: str = ""
    password: str = ""

    skill_level: str = "Beginner"
    study_hours_per_day: int = 2
    profile_image: str = "avatar.png"
    bio: str = ""

    streak: int = 0

    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # -----------------------------
    # Database Helper Methods
    # -----------------------------
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(Config.DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_by_id(cls, user_id: int):
        conn = cls.get_db_connection()
        user_data = conn.execute(
            """
            SELECT u.*, p.streak 
            FROM users u 
            LEFT JOIN progress p ON u.id = p.user_id 
            WHERE u.id = ?
            """,
            (user_id,)
        ).fetchone()
        conn.close()

        if user_data:
            return cls(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
                skill_level=user_data["skill_level"],
                study_hours_per_day=user_data["study_hours_per_day"],
                profile_image=user_data["profile_image"] or "avatar.png",
                bio=user_data["bio"] or "",
                streak=user_data["streak"] or 0,
                created_at=str(user_data["created_at"])
            )
        return None

    @classmethod
    def get_by_email(cls, email: str):
        conn = cls.get_db_connection()
        user_data = conn.execute(
            """
            SELECT u.*, p.streak 
            FROM users u 
            LEFT JOIN progress p ON u.id = p.user_id 
            WHERE u.email = ?
            """,
            (email,)
        ).fetchone()
        conn.close()

        if user_data:
            return cls(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
                skill_level=user_data["skill_level"],
                study_hours_per_day=user_data["study_hours_per_day"],
                profile_image=user_data["profile_image"] or "avatar.png",
                bio=user_data["bio"] or "",
                streak=user_data["streak"] or 0,
                created_at=str(user_data["created_at"])
            )
        return None

    @classmethod
    def create(cls, name, email, hashed_password, skill_level="Beginner", study_hours=2):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        # Insert user
        cursor.execute(
            """
            INSERT INTO users (name, email, password, skill_level, study_hours_per_day)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, hashed_password, skill_level, study_hours)
        )
        user_id = cursor.lastrowid

        # Initialize progress row for user
        cursor.execute(
            "INSERT INTO progress (user_id) VALUES (?)",
            (user_id,)
        )

        # Initialize learning DNA row for user
        cursor.execute(
            "INSERT INTO learning_dna (user_id) VALUES (?)",
            (user_id,)
        )

        conn.commit()
        conn.close()

        return cls.get_by_id(user_id)

    # -----------------------------
    # Update Methods
    # -----------------------------
    def update_skill_level(self, level):
        self.skill_level = level

    def update_study_hours(self, hours):
        if hours > 0:
            self.study_hours_per_day = hours

    def increase_streak(self):
        self.streak += 1

    def reset_streak(self):
        self.streak = 0

    # -----------------------------
    # Save Model Changes to DB
    # -----------------------------
    def save(self):
        conn = self.get_db_connection()
        conn.execute(
            """
            UPDATE users 
            SET name = ?, skill_level = ?, study_hours_per_day = ?, profile_image = ?, bio = ?
            WHERE id = ?
            """,
            (self.name, self.skill_level, self.study_hours_per_day, self.profile_image, self.bio, self.id)
        )
        conn.execute(
            "UPDATE progress SET streak = ? WHERE user_id = ?",
            (self.streak, self.id)
        )
        conn.commit()
        conn.close()

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
            "profile_image": self.profile_image,
            "bio": self.bio,
            "streak": self.streak,
            "created_at": self.created_at
        }

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):
        return f"{self.name} ({self.email})"