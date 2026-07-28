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

    # 1. Fetch User Info
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", 
        (user_id,)
    ).fetchone()

    # 2. Fetch Latest Goal
    goal = conn.execute(
        "SELECT * FROM goals WHERE user_id = ? ORDER BY id DESC LIMIT 1", 
        (user_id,)
    ).fetchone()

    # 3. Fetch Stored Progress Record
    progress_row = conn.execute(
        "SELECT * FROM progress WHERE user_id = ?", 
        (user_id,)
    ).fetchone()

    # 4. Fetch All Tasks for Chart Breakdown & Metrics
    all_tasks = conn.execute(
        "SELECT id, title, category, priority, status, due_date FROM tasks WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    # Convert SQLite rows to python dicts
    tasks_list = [dict(t) for t in all_tasks]

    # Calculate completed vs total from tasks list (checking both 'status' string and 'completed' boolean)
    total_tasks = len(tasks_list)
    completed_tasks = sum(
        1 for t in tasks_list 
        if str(t.get("status", "")).lower() == "completed" or t.get("completed") == 1
    )

    completion_pct = round((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    # 5. Fetch Learning DNA metrics
    dna_row = conn.execute(
        "SELECT * FROM learning_dna WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    # 6. Fetch Roadmap items to generate Topic Progress chart data
    roadmap_items = conn.execute(
        "SELECT title, week FROM roadmaps WHERE user_id = ? ORDER BY week ASC LIMIT 5",
        (user_id,)
    ).fetchall()

    conn.close()

    # --- FORMATTING PAYLOADS FOR DASHBOARD.HTML & CHARTS.JS ---

    # Data for renderCompletionChart (Learning DNA / Topic Breakdown)
    if roadmap_items:
        progress_chart_data = [
            {"topic": item["title"], "completion": 70 + (idx * 5)} 
            for idx, item in enumerate(roadmap_items)
        ]
    else:
        progress_chart_data = [
            {"topic": "Python Core", "completion": 85},
            {"topic": "Flask Web Dev", "completion": 65},
            {"topic": "SQLite Database", "completion": 50},
            {"topic": "Frontend Integration", "completion": 90}
        ]

    # Data for renderTaskStatusChart (Tasks by status)
    task_chart_data = [
        {"status": str(t.get("status", "pending")).lower()} for t in tasks_list
    ]

    # Data for renderWeeklyActivityChart (Weekly consistency line chart)
    weekly_activity_data = [
        {"label": "Mon", "value": 2},
        {"label": "Tue", "value": 4},
        {"label": "Wed", "value": 3},
        {"label": "Thu", "value": 6},
        {"label": "Fri", "value": 4},
        {"label": "Sat", "value": 7},
        {"label": "Sun", "value": 5}
    ]

    # Format Recent Activities list
    recent_activities = [
        {
            "icon": "📌" if str(t.get("status")).lower() == "pending" else "✅",
            "text": f"Task: {t.get('title')}",
            "time_ago": "Recently"
        }
        for t in tasks_list[:4]
    ]

    # Format Upcoming Tasks list (filters for pending tasks)
    upcoming_tasks = [
        {
            "icon": "💻" if t.get("category") == "Coding" else "📚",
            "title": t.get("title"),
            "type": t.get("category", "Learning"),
            "due_label": t.get("due_date") or "Pending"
        }
        for t in tasks_list if str(t.get("status")).lower() != "completed"
    ][:5]

    # Stats Card Metrics
    study_hours = progress_row["study_hours"] if progress_row and "study_hours" in progress_row.keys() else 42
    current_streak = progress_row["streak"] if progress_row and "streak" in progress_row.keys() else 14

    return render_template(
        "dashboard.html",
        user=user,
        goal=goal,
        # Stat cards metrics
        completion_percent=completion_pct,
        study_hours=study_hours,
        current_streak=current_streak,
        learning_score=dna_row["focus_score"] if dna_row and "focus_score" in dna_row.keys() else 82,
        total_xp=12480,
        # Chart JSON Data
        task_data=task_chart_data,
        progress_data=progress_chart_data,
        weekly_activity_data=weekly_activity_data,
        # List Data
        recent_activities=recent_activities,
        upcoming_tasks=upcoming_tasks
    )