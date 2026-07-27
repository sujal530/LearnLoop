import sqlite3

from flask import Blueprint, flash, redirect, render_template, session, url_for

from config import Config
from utils.decorators import login_required

auth_bp = Blueprint("auth", __name__)


def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@auth_bp.route("/auth")
@login_required
def dashboard():
    user_id = session["user_id"]
    conn = None

    try:
        conn = get_db()

        # Fetch logged-in user
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()

        if not user:
            session.clear()
            flash("Session expired. Please log in again.", "warning")
            return redirect(url_for("auth.login"))

        # Fetch most recent goal
        goal = conn.execute(
            """
            SELECT * FROM goals
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

        # Fetch task counts
        completed_tasks = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1",
            (user_id,),
        ).fetchone()[0]

        total_tasks = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ?",
            (user_id,),
        ).fetchone()[0]

        # Fetch additional summary counts
        roadmap_count = conn.execute(
            "SELECT COUNT(*) FROM roadmaps WHERE user_id = ?",
            (user_id,),
        ).fetchone()[0]

        quiz_count = conn.execute(
            "SELECT COUNT(*) FROM quiz_history WHERE user_id = ?",
            (user_id,),
        ).fetchone()[0]

        # Fetch existing progress row
        progress = conn.execute(
            "SELECT * FROM progress WHERE user_id = ?", (user_id,)
        ).fetchone()

        if not progress:
            # Create a fresh progress row for this user
            conn.execute(
                """
                INSERT INTO progress (user_id, completed_tasks, total_tasks, study_hours, streak)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, completed_tasks, total_tasks, 0, 0),
            )
            conn.commit()
        else:
            # Synchronize live task counts into the progress table
            conn.execute(
                """
                UPDATE progress
                SET completed_tasks = ?,
                    total_tasks     = ?
                WHERE user_id = ?
                """,
                (completed_tasks, total_tasks, user_id),
            )
            conn.commit()

        # Reload progress row so template always receives the latest values
        progress = conn.execute(
            "SELECT * FROM progress WHERE user_id = ?", (user_id,)
        ).fetchone()

        return render_template(
            "dashboard.html",
            user=user,
            goal=goal,
            progress=progress,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            roadmap_count=roadmap_count,
            quiz_count=quiz_count,
        )

    except sqlite3.Error:
        flash("A database error occurred. Please try again.", "danger")
        return redirect(url_for("auth.login"))

    finally:
        if conn:
            conn.close()