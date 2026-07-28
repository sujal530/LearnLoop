"""
routes/auth.py

Authentication blueprint for LearnLoop AI (Login, Register, Logout)
"""

import sqlite3
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import generate_password_hash, check_password_hash


from config import Config
from utils.decorators import login_required


auth_bp = Blueprint("auth", __name__)


def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# LOGIN
# -------------------------



# -----------------------------
# Login Route
# -----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, redirect directly to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()

        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return render_template("login.html")

        user = User.get_by_email(email)

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))

        else:
            flash(
                "Invalid email or password",
                "danger"
            )


    return render_template("login.html")




# -------------------------
# REGISTER
# -------------------------


# -----------------------------
# Register Route
# -----------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        name = (
            request.form.get("full_name")
            or request.form.get("name")
            or request.form.get("username")
            or ""
        ).strip()
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()
        confirm_password = (request.form.get("confirm_password") or "").strip()
        skill_level = request.form.get("skill_level", "Beginner")
        study_hours = int(request.form.get("study_hours_per_day", 2))

        # 1. Validation: Required fields
        if not email or not password:
            flash("Email and password are required.", "warning")
            return render_template("register.html")

        # 2. Validation: Passwords match
        if confirm_password and password != confirm_password:
            flash("Passwords do not match.", "warning")
            return render_template("register.html")

        # Check existing user
        existing_user = User.get_by_email(email)
        if existing_user:
            flash("That email is already registered. Try logging in instead.", "warning")
            return redirect(url_for("auth.login"))

        hashed_pw = generate_password_hash(password)

        try:
            # Use User model helper to create user + progress + learning_dna records
            new_user = User.create(
                name=name or "Learner",
                email=email,
                hashed_password=hashed_pw,
                skill_level=skill_level,
                study_hours=study_hours
            )

            if new_user:
                session["user_id"] = new_user.id
                session["user_name"] = new_user.name
                flash("Account created successfully! Welcome to LearnLoop AI.", "success")
                return redirect(url_for("dashboard.dashboard"))

        except sqlite3.IntegrityError:
            flash("That email is already registered.", "warning")
        except Exception as e:
            flash(f"Error creating account: {e}", "danger")




    return render_template("register.html")




# -------------------------
# DASHBOARD
# -------------------------
@auth_bp.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    conn = None

    try:

        conn = get_db()


        user = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()


        if not user:

            session.clear()

            flash(
                "Session expired. Please login again.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )



        goal = conn.execute(
            """
            SELECT *
            FROM goals
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()



        completed_tasks = conn.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE user_id = ?
            AND completed = 1
            """,
            (user_id,)
        ).fetchone()[0]



        total_tasks = conn.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]



        roadmap_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM roadmaps
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]



        quiz_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM quiz_history
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]



        progress = conn.execute(
            """
            SELECT *
            FROM progress
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()



        if not progress:

            conn.execute(
                """
                INSERT INTO progress
                (
                    user_id,
                    completed_tasks,
                    total_tasks,
                    study_hours,
                    streak
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    completed_tasks,
                    total_tasks,
                    0,
                    0
                )
            )

        else:

            conn.execute(
                """
                UPDATE progress
                SET completed_tasks=?,
                    total_tasks=?
                WHERE user_id=?
                """,
                (
                    completed_tasks,
                    total_tasks,
                    user_id
                )
            )


        conn.commit()


        progress = conn.execute(
            """
            SELECT *
            FROM progress
            WHERE user_id=?
            """,
            (user_id,)
        ).fetchone()



        return render_template(
            "dashboard.html",
            user=user,
            goal=goal,
            progress=progress,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            roadmap_count=roadmap_count,
            quiz_count=quiz_count
        )



    except sqlite3.Error:

        flash(
            "Database error occurred",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )



    finally:

        if conn:
            conn.close()



# -------------------------
# LOGOUT
# -------------------------

# -----------------------------
# Logout Route
# -----------------------------

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )