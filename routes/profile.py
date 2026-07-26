from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import sqlite3
from config import Config

profile_bp = Blueprint("profile", __name__)

DATABASE = Config.DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------
# View Profile
# --------------------------------
@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    goal = conn.execute(
        """
        SELECT * FROM goals
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (session["user_id"],)
    ).fetchone()

    progress = conn.execute(
        "SELECT * FROM progress WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user,
        goal=goal,
        progress=progress
    )


# --------------------------------
# Edit Profile
# --------------------------------
@profile_bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        conn.execute(
            """
            UPDATE users
            SET name=?, email=?
            WHERE id=?
            """,
            (
                name,
                email,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("profile.profile"))

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_profile.html",
        user=user
    )


# --------------------------------
# Change Password
# --------------------------------
@profile_bp.route("/profile/password", methods=["GET", "POST"])
def change_password():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        new_password = request.form["password"]

        conn = get_db()

        conn.execute(
            """
            UPDATE users
            SET password=?
            WHERE id=?
            """,
            (
                new_password,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        flash("Password changed successfully!", "success")

        return redirect(url_for("profile.profile"))

    return render_template("change_password.html")
