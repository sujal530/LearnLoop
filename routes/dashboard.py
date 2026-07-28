"""
routes/dashboard.py

Blueprint for handling main dashboard view, progress tracking, and Learning DNA stats.
"""

import sqlite3
from flask import Blueprint, render_template, session, redirect, url_for
from config import Config

dashboard_bp = Blueprint("dashboard", __name__)


def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    conn = get_db_connection()

    # Fetch User Info
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", 
        (user_id,)
    ).fetchone()

    # Fetch Latest Goal
    goal = conn.execute(
        "SELECT * FROM goals WHERE user_id = ? ORDER BY id DESC LIMIT 1", 
        (user_id,)
    ).fetchone()

    # Fetch Stored Progress Record
    progress_row = conn.execute(
        "SELECT * FROM progress WHERE user_id = ?", 
        (user_id,)
    ).fetchone()

    # Dynamic Task Counts directly from task table
    tasks_count = conn.execute(
        "SELECT COUNT(*) AS total, SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) AS completed FROM tasks WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    # Fetch Learning DNA metrics
    dna_row = conn.execute(
        "SELECT * FROM learning_dna WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    # Fetch Recent Tasks (for quick display)
    recent_tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,)
    ).fetchall()

    conn.close()

    # Calculate Progress Data
    total_tasks = tasks_count["total"] if tasks_count and tasks_count["total"] > 0 else (progress_row["total_tasks"] if progress_row else 0)
    completed_tasks = tasks_count["completed"] if tasks_count and tasks_count["completed"] is not None else (progress_row["completed_tasks"] if progress_row else 0)

    completion_pct = round((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    progress_data = {
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "study_hours": progress_row["study_hours"] if progress_row else 0,
        "streak": progress_row["streak"] if progress_row else 0,
        "completion": completion_pct
    }

    # Prepare Learning DNA Data
    learning_dna_data = {
        "consistency": dna_row["consistency"] if dna_row else 80,
        "velocity": dna_row["velocity"] if dna_row else 75,
        "retention": dna_row["retention"] if dna_row else 85,
        "focus_score": dna_row["focus_score"] if dna_row else 90
    }

    return render_template(
        "dashboard.html",
        user=user,
        goal=goal,
        progress=progress_data,
        learning_dna=learning_dna_data,
        recent_tasks=[dict(t) for t in recent_tasks]
    )