import sqlite3
from config import Config

def migrate():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN category TEXT DEFAULT 'Learning'")
        conn.commit()
        print("✅ Added 'category' column to tasks table!")
    except sqlite3.OperationalError as e:
        print(f"Note: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()