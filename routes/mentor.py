from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import google.generativeai as genai
from config import Config


mentor_bp = Blueprint("mentor", __name__)

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel(Config.GEMINI_MODEL)


# -----------------------------
# Mentor Page
# -----------------------------
@mentor_bp.route("/mentor")
def mentor():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("mentor.html")


# -----------------------------
# Chat API
# -----------------------------
@mentor_bp.route("/mentor/chat", methods=["POST"])
def mentor_chat():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    prompt = data.get("message", "").strip()

    if not prompt:
        return jsonify({
            "response": "Please enter a question."
        })

    try:

        system_prompt = f"""
You are LearnLoop AI.

You are a professional AI mentor.

Your job is to:
- Explain concepts in simple language.
- Answer student doubts.
- Give examples.
- Suggest learning resources.
- Encourage the learner.
- Keep answers concise and beginner-friendly.

Student Question:
{prompt}
"""

        response = model.generate_content(system_prompt)

        return jsonify({
            "response": response.text
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        }), 500


# -----------------------------
# AI Quiz Generator
# -----------------------------
@mentor_bp.route("/mentor/quiz", methods=["POST"])
def generate_quiz():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    topic = data.get("topic", "")

    prompt = f"""
Generate 5 multiple-choice questions on {topic}.

Format:

Question:
A.
B.
C.
D.
Answer:
"""

    try:

        response = model.generate_content(prompt)

        return jsonify({
            "quiz": response.text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# AI Roadmap Suggestion
# -----------------------------
@mentor_bp.route("/mentor/roadmap", methods=["POST"])
def roadmap():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    goal = data.get("goal")
    level = data.get("level")
    study_time = data.get("study_time")

    prompt = f"""
Create a weekly learning roadmap.

Goal:
{goal}

Skill Level:
{level}

Daily Study Time:
{study_time}

Return:
Week 1
Week 2
Week 3
...
"""

    try:

        response = model.generate_content(prompt)

        return jsonify({
            "roadmap": response.text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500