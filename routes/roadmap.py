import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import Config

roadmap_bp = Blueprint("roadmap", __name__)

def get_db():
    conn = sqlite3.connect(Config.DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

@roadmap_bp.route("/roadmap", methods=["GET", "POST"])
def roadmap():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    conn = get_db()

    # 1. Check if user has an existing goal
    goal_row = conn.execute(
        "SELECT * FROM goals WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,)
    ).fetchone()

    # 2. Fetch existing roadmap entries
    roadmaps = conn.execute(
        "SELECT * FROM roadmaps WHERE user_id = ? ORDER BY week ASC",
        (user_id,)
    ).fetchall()

    # 3. If no roadmap exists, auto-generate starter roadmap items
    if not roadmaps:
        default_goal_id = goal_row["id"] if goal_row else None
        
        # Insert initial default learning roadmap
        starter_weeks = [
            (user_id, default_goal_id, 1, "Fundamentals & Basics", "Understand basic syntax, core concepts, and environment setup."),
            (user_id, default_goal_id, 2, "Core Applications & Logic", "Build hands-on practice modules, practice data manipulation, and simple projects."),
            (user_id, default_goal_id, 3, "Advanced Topics & Integration", "Learn state management, APIs, databases, and architectural patterns."),
            (user_id, default_goal_id, 4, "Capstone Project & Deployment", "Develop a full end-to-end project and deploy it to a live environment.")
        ]

        conn.executemany(
            """
            INSERT INTO roadmaps (user_id, goal_id, week, title, content)
            VALUES (?, ?, ?, ?, ?)
            """,
            starter_weeks
        )
        conn.commit()

        # Re-fetch the freshly inserted roadmap
        roadmaps = conn.execute(
            "SELECT * FROM roadmaps WHERE user_id = ? ORDER BY week ASC",
            (user_id,)
        ).fetchall()

    conn.close()
    return render_template("roadmap.html", roadmaps=roadmaps, goal=goal_row)