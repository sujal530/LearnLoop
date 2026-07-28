"""
seed_roadmap.py
Populates the roadmaps table with sample data for testing.
"""

import sqlite3
from config import Config


def seed():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    # Sample roadmap weeks for user_id = 1
    weeks = [
        (1, 1, "Python Basics", "Variables, Control Flow, Functions, and Modules."),
        (1, 2, "Data Structures & OOP", "Lists, Dicts, Classes, and Objects."),
        (1, 3, "Flask Web Development", "Routes, Templates, SQLite integration, and Blueprints."),
        (1, 4, "Deployment & Capstone", "Building full-stack projects and deploying live.")
    ]

    cursor.executemany(
        "INSERT INTO roadmaps (user_id, week, title, content) VALUES (?, ?, ?, ?)",
        weeks
    )
    conn.commit()
    conn.close()
    print("✅ Roadmap seeded successfully for user 1!")


if __name__ == "__main__":
    seed()