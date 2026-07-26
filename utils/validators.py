"""
validators.py
Validation functions for LearnLoop AI
"""

import re


# ----------------------------------
# Name Validation
# ----------------------------------
def validate_name(name):

    if not name:
        return False, "Name is required."

    if len(name) < 3:
        return False, "Name must be at least 3 characters."

    return True, ""


# ----------------------------------
# Email Validation
# ----------------------------------
def validate_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not email:
        return False, "Email is required."

    if not re.match(pattern, email):
        return False, "Invalid email address."

    return True, ""


# ----------------------------------
# Password Validation
# ----------------------------------
def validate_password(password):

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain one lowercase letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain one number."

    return True, ""


# ----------------------------------
# Learning Goal Validation
# ----------------------------------
def validate_goal(goal):

    if not goal:
        return False, "Learning goal is required."

    if len(goal) < 5:
        return False, "Goal description is too short."

    return True, ""


# ----------------------------------
# Skill Level Validation
# ----------------------------------
def validate_skill_level(level):

    levels = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    if level not in levels:
        return False, "Invalid skill level."

    return True, ""


# ----------------------------------
# Study Time Validation
# ----------------------------------
def validate_study_time(hours):

    try:
        hours = int(hours)

        if hours <= 0:
            return False, "Study time must be greater than 0."

        if hours > 24:
            return False, "Study time cannot exceed 24 hours."

        return True, ""

    except ValueError:
        return False, "Study time must be a number."


# ----------------------------------
# Deadline Validation
# ----------------------------------
def validate_deadline(deadline):

    if not deadline:
        return False, "Deadline is required."

    return True, ""


# ----------------------------------
# Quiz Topic Validation
# ----------------------------------
def validate_quiz_topic(topic):

    if not topic:
        return False, "Quiz topic cannot be empty."

    if len(topic) < 2:
        return False, "Quiz topic is too short."

    return True, ""


# ----------------------------------
# AI Prompt Validation
# ----------------------------------
def validate_prompt(prompt):

    if not prompt:
        return False, "Prompt cannot be empty."

    if len(prompt) < 5:
        return False, "Prompt is too short."

    return True, ""


# ----------------------------------
# Generic Required Field
# ----------------------------------
def required(value, field_name):

    if not value:
        return False, f"{field_name} is required."

    return True, ""
