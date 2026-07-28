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
        CREATE TABLE IF NOT EXISTS mentor_chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

           FOREIGN KEY(user_id)
           REFERENCES users(id)
           ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print(" Database initialized successfully!")

if __name__ == "__main__":
    init_db()