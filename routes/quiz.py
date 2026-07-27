import sqlite3
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
)
import google.generativeai as genai
from config import Config

quiz_bp = Blueprint("quiz", __name__)

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel(Config.GEMINI_MODEL)

DATABASE = Config.DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Quiz Page
# -----------------------------
@quiz_bp.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Passing quiz_question=None prevents Jinja2 UndefinedError in quiz.html
    return render_template("quiz.html", quiz_question=None)


# -----------------------------
# Generate Quiz
# -----------------------------
@quiz_bp.route("/quiz/generate", methods=["POST"])
def generate_quiz():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    topic = data.get("topic", "General Knowledge")
    difficulty = data.get("difficulty", "Beginner")

    prompt = f"""
Generate exactly 5 multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY in this format:

Question 1:
A.
B.
C.
D.
Answer:

Question 2:
...

Do not include explanations.
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"quiz": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Submit Quiz
# -----------------------------
@quiz_bp.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    try:
        score = int(data.get("score", 0))
        total = int(data.get("total", 5))
    except (ValueError, TypeError):
        score, total = 0, 5

    # Prevent division by zero
    percentage = round((score / total) * 100) if total > 0 else 0

    conn = get_db()

    # Ensure table exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            total INTEGER,
            percentage INTEGER
        )
    """)

    # Record history
    conn.execute("""
        INSERT INTO quiz_history(
            user_id,
            score,
            total,
            percentage
        )
        VALUES(?,?,?,?)
    """, (session["user_id"], score, total, percentage))

    conn.commit()

    # Update user completed tasks in progress table
    progress = conn.execute("""
        SELECT *
        FROM progress
        WHERE user_id=?
    """, (session["user_id"],)).fetchone()

    if progress:
        conn.execute("""
            UPDATE progress
            SET completed_tasks = completed_tasks + 1
            WHERE user_id=?
        """, (session["user_id"],))
        conn.commit()

    conn.close()

    return jsonify({
        "score": score,
        "total": total,
        "percentage": percentage,
        "message": "Quiz Submitted Successfully"
    })


# -----------------------------
# Quiz History (HTML Page)
# -----------------------------
@quiz_bp.route("/quiz/history")
def quiz_history():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db()

    history = conn.execute("""
        SELECT *
        FROM quiz_history
        WHERE user_id=?
        ORDER BY id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template("quiz_history.html", history=history)


# -----------------------------
# Quiz History (JSON API)
# -----------------------------
@quiz_bp.route("/api/quiz/history")
def quiz_api():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()

    history = conn.execute("""
        SELECT score, total, percentage
        FROM quiz_history
        WHERE user_id=?
        ORDER BY id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    result = [
        {
            "score": row["score"],
            "total": row["total"],
            "percentage": row["percentage"]
        }
        for row in history
    ]

    return jsonify(result)