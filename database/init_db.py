import sys
import os

# Add root directory to sys.path so it can find config.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
from config import Config

def init_db():
    db_path = Config.DATABASE
    
    # Ensure database folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tasks table with all required columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            roadmap_id INTEGER DEFAULT 0,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'Learning',
            priority TEXT DEFAULT 'Medium',
            estimated_time INTEGER DEFAULT 60,
            status TEXT DEFAULT 'pending',
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print(" Database initialized successfully!")

if __name__ == "__main__":
    init_db()