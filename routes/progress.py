from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import sqlite3
from config import Config

progress_bp = Blueprint("progress", __name__)

DATABASE = Config.DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------
# Progress Dashboard
# ---------------------------------
@progress_bp.route("/progress")
def progress():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db()

    progress = conn.execute(
        """
        SELECT *
        FROM progress
        WHERE user_id=?
        """,
        (session["user_id"],)
    ).fetchone()

    conn.close()

    if progress:

        completion = 0

        if progress["total_tasks"] > 0:
            completion = round(
                (progress["completed_tasks"] /
                 progress["total_tasks"]) * 100
            )

        data = {
            "completed_tasks": progress["completed_tasks"],
            "total_tasks": progress["total_tasks"],
            "study_hours": progress["study_hours"],
            "streak": progress["streak"],
            "completion": completion
        }

    else:

        data = {
            "completed_tasks": 0,
            "total_tasks": 0,
            "study_hours": 0,
            "streak": 0,
            "completion": 0
        }

    return render_template(
        "progress.html",
        progress=data
    )


# ---------------------------------
# Update Progress
# ---------------------------------
@progress_bp.route("/progress/update", methods=["POST"])
def update_progress():

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    completed = int(request.form.get("completed_tasks", 0))
    total = int(request.form.get("total_tasks", 0))
    study_hours = int(request.form.get("study_hours", 0))
    streak = int(request.form.get("streak", 0))

    conn = get_db()

    exists = conn.execute(
        """
        SELECT id
        FROM progress
        WHERE user_id=?
        """,
        (session["user_id"],)
    ).fetchone()

    if exists:

        conn.execute(
            """
            UPDATE progress
            SET completed_tasks=?,
                total_tasks=?,
                study_hours=?,
                streak=?
            WHERE user_id=?
            """,
            (
                completed,
                total,
                study_hours,
                streak,
                session["user_id"]
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO progress(
                user_id,
                completed_tasks,
                total_tasks,
                study_hours,
                streak
            )
            VALUES(?,?,?,?,?)
            """,
            (
                session["user_id"],
                completed,
                total,
                study_hours,
                streak
            )
        )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Progress Updated Successfully"
    })


# ---------------------------------
# Progress API
# ---------------------------------
@progress_bp.route("/api/progress")
def progress_api():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()

    progress = conn.execute(
        """
        SELECT *
        FROM progress
        WHERE user_id=?
        """,
        (session["user_id"],)
    ).fetchone()

    conn.close()

    if not progress:
        return jsonify({
            "completed_tasks": 0,
            "total_tasks": 0,
            "study_hours": 0,
            "streak": 0,
            "completion": 0
        })

    completion = 0

    if progress["total_tasks"] > 0:
        completion = round(
            (progress["completed_tasks"] /
             progress["total_tasks"]) * 100
        )

    return jsonify({
        "completed_tasks": progress["completed_tasks"],
        "total_tasks": progress["total_tasks"],
        "study_hours": progress["study_hours"],
        "streak": progress["streak"],
        "completion": completion
    })
    