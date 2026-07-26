"""
database/init_db.py

Initializes the LearnLoop AI SQLite database.
"""

import os
import sqlite3
from config import Config


def init_db():
    # Create database folder if it doesn't exist
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)

    conn = sqlite3.connect(Config.DATABASE)

    # Enable Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON")

    cursor = conn.cursor()

    # =====================================================
    # USERS
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        skill_level TEXT DEFAULT 'Beginner',
        study_hours_per_day INTEGER DEFAULT 2,
        profile_image TEXT,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # GOALS
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal TEXT NOT NULL,
        deadline TEXT,
        status TEXT DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """)

    # =====================================================
    # ROADMAPS
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_id INTEGER,
        week INTEGER,
        title TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

        FOREIGN KEY(goal_id)
        REFERENCES goals(id)
        ON DELETE CASCADE
    )
    """)

    # =====================================================
    # TASKS
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        roadmap_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT DEFAULT 'Medium',
        estimated_time INTEGER DEFAULT 60,
        status TEXT DEFAULT 'Pending',
        completed INTEGER DEFAULT 0,
        due_date TEXT,
        completed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

        FOREIGN KEY(roadmap_id)
        REFERENCES roadmaps(id)
        ON DELETE CASCADE
    )
    """)

    # =====================================================
    # PROGRESS
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        completed_tasks INTEGER DEFAULT 0,
        total_tasks INTEGER DEFAULT 0,
        completion_percentage REAL DEFAULT 0,
        study_hours REAL DEFAULT 0,
        streak INTEGER DEFAULT 0,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """)

    # =====================================================
    # QUIZ HISTORY
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        difficulty TEXT,
        score INTEGER,
        total_questions INTEGER,
        percentage REAL,
        time_taken INTEGER,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """)

    # =====================================================
    # LEARNING DNA
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_dna (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        consistency INTEGER DEFAULT 0,
        confidence INTEGER DEFAULT 0,
        understanding INTEGER DEFAULT 0,
        quiz_score INTEGER DEFAULT 0,
        study_hours INTEGER DEFAULT 0,
        learning_dna_score INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

    print("✅ LearnLoop Database Initialized Successfully.")


if __name__ == "__main__":
    init_db()