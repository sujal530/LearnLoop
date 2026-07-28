"""
models/roadmap.py

Database operations for Roadmaps and Milestones.
"""

import sqlite3
from config import Config


class Roadmap:
    def __init__(self, id, user_id, title, duration_weeks, created_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.duration_weeks = duration_weeks
        self.created_at = created_at

    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_latest_by_user(cls, user_id):
        """Fetch the user's most recently created roadmap."""
        conn = cls.get_db()
        row = conn.execute(
            "SELECT * FROM roadmaps WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        conn.close()

        if row:
            return cls(
                id=row["id"],
                user_id=row["user_id"],
                title=row["title"],
                duration_weeks=row["duration_weeks"],
                created_at=row["created_at"] if "created_at" in row.keys() else None
            )
        return None

    @classmethod
    def get_milestones(cls, roadmap_id):
        """Fetch all milestones attached to a roadmap."""
        conn = cls.get_db()
        rows = conn.execute(
            "SELECT * FROM milestones WHERE roadmap_id = ? ORDER BY id ASC",
            (roadmap_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def create(cls, user_id, title, duration_weeks, milestones=None):
        """Create a new roadmap and save associated milestones."""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO roadmaps (user_id, title, duration_weeks) VALUES (?, ?, ?)",
            (user_id, title, duration_weeks)
        )
        roadmap_id = cursor.lastrowid

        if milestones:
            for idx, milestone_title in enumerate(milestones, start=1):
                cursor.execute(
                    "INSERT INTO milestones (roadmap_id, title, week_number, completed) VALUES (?, ?, ?, 0)",
                    (roadmap_id, milestone_title, idx)
                )

        conn.commit()
        conn.close()
        return cls.get_latest_by_user(user_id)

    @classmethod
    def toggle_milestone(cls, milestone_id):
        """Toggle completion status of a milestone."""
        conn = cls.get_db()
        row = conn.execute("SELECT completed FROM milestones WHERE id = ?", (milestone_id,)).fetchone()
        if not row:
            conn.close()
            return None

        new_status = 0 if row["completed"] else 1
        conn.execute("UPDATE milestones SET completed = ? WHERE id = ?", (new_status, milestone_id))
        conn.commit()
        conn.close()
        return new_status