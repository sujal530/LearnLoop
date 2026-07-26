from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3
from config import Config

dashboard_bp = Blueprint("dashboard", __name__)

DATABASE = Config.DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db()

    # User Information
    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    # User Goal
    goal = conn.execute(
        "SELECT * FROM goals WHERE user_id=? ORDER BY id DESC LIMIT 1",
        (session["user_id"],)
    ).fetchone()

    # User Progress
    progress = conn.execute(
        "SELECT * FROM progress WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    # Default values if no progress exists
    dashboard_data = {
        "completed_tasks": 0,
        "total_tasks": 0,
        "study_hours": 0,
        "streak": 0,
        "completion": 0
    }

    if progress:
        dashboard_data["completed_tasks"] = progress["completed_tasks"]
        dashboard_data["total_tasks"] = progress["total_tasks"]
        dashboard_data["study_hours"] = progress["study_hours"]
        dashboard_data["streak"] = progress["streak"]

        if progress["total_tasks"] > 0:
            dashboard_data["completion"] = round(
                (progress["completed_tasks"] /
                 progress["total_tasks"]) * 100
            )

    return render_template(
        "dashboard.html",
        user=user,
        goal=goal,
        progress=dashboard_data
    )