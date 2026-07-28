"""
routes/roadmap.py

Blueprint for managing dynamic AI-generated learning roadmaps and milestones.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from models.roadmap import Roadmap
from ai.ai_service import ai_service

roadmap_bp = Blueprint("roadmap", __name__)


# -----------------------------
# Active Roadmap View
# -----------------------------
@roadmap_bp.route("/roadmap")
def roadmap():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    
    # Get the latest generated roadmap or all user roadmaps
    current_roadmap = Roadmap.get_latest_by_user(user_id)
    milestones = Roadmap.get_milestones(current_roadmap.id) if current_roadmap else []

    return render_template(
        "roadmap.html", 
        roadmap=current_roadmap, 
        milestones=milestones
    )


# -----------------------------
# Generate AI Roadmap
# -----------------------------
@roadmap_bp.route("/roadmap/generate", methods=["POST"])
def generate_roadmap():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    goal_title = request.form.get("goal_title", "").strip()
    target_weeks = int(request.form.get("target_weeks", 4))

    if not goal_title:
        flash("Please enter a learning goal or topic to generate a roadmap.", "warning")
        return redirect(url_for("roadmap.roadmap"))

    # Prompt AI engine to generate structured phases/milestones
    ai_roadmap_data = ai_service.generate_roadmap(goal_title, target_weeks)

    if ai_roadmap_data:
        # Save new roadmap and attached milestones to database
        new_roadmap = Roadmap.create(
            user_id=user_id,
            title=goal_title,
            duration_weeks=target_weeks,
            milestones=ai_roadmap_data.get("milestones", [])
        )
        flash("New roadmap generated successfully!", "success")
    else:
        flash("Could not generate roadmap right now. Please try again.", "danger")

    return redirect(url_for("roadmap.roadmap"))


# -----------------------------
# Toggle Milestone Status
# -----------------------------
@roadmap_bp.route("/roadmap/milestone/<int:milestone_id>/toggle", methods=["POST"])
def toggle_milestone(milestone_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    updated_status = Roadmap.toggle_milestone(milestone_id)
    if updated_status is not None:
        return jsonify({"success": True, "completed": updated_status})

    return jsonify({"error": "Milestone not found"}), 404