"""
routes/mentor.py

Blueprint for AI Mentor route handlers and chat endpoints.
"""

import sqlite3
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from config import Config
from ai.ai_service import ai_service

mentor_bp = Blueprint("mentor", __name__)


def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Mentor Page
# -----------------------------
@mentor_bp.route("/mentor", methods=["GET", "POST"])
def mentor():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # Handle standard HTML form submission fallback
    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if user_msg:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Save user message
            cursor.execute(
                "INSERT INTO mentor_chats (user_id, sender, message) VALUES (?, ?, ?)",
                (user_id, "user", user_msg)
            )

            # Get past chat history for context
            history_rows = cursor.execute(
                "SELECT sender, message AS text FROM mentor_chats WHERE user_id = ? ORDER BY id DESC LIMIT 6",
                (user_id,)
            ).fetchall()
            history = [dict(r) for r in reversed(history_rows)]

            # Generate AI response
            ai_reply = ai_service.mentor_chat(user_msg, history)

            # Save AI response
            cursor.execute(
                "INSERT INTO mentor_chats (user_id, sender, message) VALUES (?, ?, ?)",
                (user_id, "mentor", ai_reply)
            )
            conn.commit()
            conn.close()

        return redirect(url_for("mentor.mentor"))

    # Fetch user chat history for template rendering
    conn = get_db_connection()
    chat_rows = conn.execute(
        """
        SELECT sender, message AS text, 
               strftime('%H:%M', created_at) AS time_ago 
        FROM mentor_chats 
        WHERE user_id = ? 
        ORDER BY id ASC
        """,
        (user_id,)
    ).fetchall()
    conn.close()

    chat_history = [dict(row) for row in chat_rows]

    return render_template("mentor.html", chat_history=chat_history)


# -----------------------------
# AJAX Chat API
# -----------------------------
@mentor_bp.route("/mentor/chat", methods=["POST"])
def mentor_chat():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    data = request.get_json() or {}
    prompt = data.get("message", "").strip()

    if not prompt:
        return jsonify({"response": "Please enter a question."})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Save user message
        cursor.execute(
            "INSERT INTO mentor_chats (user_id, sender, message) VALUES (?, ?, ?)",
            (user_id, "user", prompt)
        )

        # Get recent context
        history_rows = cursor.execute(
            "SELECT sender, message AS text FROM mentor_chats WHERE user_id = ? ORDER BY id DESC LIMIT 6",
            (user_id,)
        ).fetchall()
        history = [dict(r) for r in reversed(history_rows)]

        # Query Gemini via AIService
        ai_reply = ai_service.mentor_chat(prompt, history)

        # Save AI reply
        cursor.execute(
            "INSERT INTO mentor_chats (user_id, sender, message) VALUES (?, ?, ?)",
            (user_id, "mentor", ai_reply)
        )
        conn.commit()
        conn.close()

        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


# -----------------------------
# AI Quiz Generator
# -----------------------------
@mentor_bp.route("/mentor/quiz", methods=["POST"])
def generate_quiz():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    topic = data.get("topic", "General Knowledge")
    difficulty = data.get("difficulty", "Beginner")

    try:
        quiz_data = ai_service.generate_quiz(topic, difficulty)
        return jsonify({"quiz": quiz_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# AI Roadmap Suggestion
# -----------------------------
@mentor_bp.route("/mentor/roadmap", methods=["POST"])
def roadmap():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    goal = data.get("goal", "Python Programming")
    level = data.get("level", "Beginner")
    study_time = data.get("study_time", 2)
    deadline = data.get("deadline", "4 Weeks")

    try:
        roadmap_content = ai_service.generate_roadmap(goal, level, study_time, deadline)
        return jsonify({"roadmap": roadmap_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500