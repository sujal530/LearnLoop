import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

auth_bp = Blueprint("auth", __name__)

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_users_columns(conn):
    cursor = conn.execute("PRAGMA table_info(users)")
    return [column[1] for column in cursor.fetchall()]

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Capture form values cleanly
        full_name = request.form.get("full_name") or request.form.get("username") or ""
        email = request.form.get("email") or ""
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        # Print to VS Code terminal to inspect input values
        print(f"\n--- REGISTER ATTEMPT ---")
        print(f"Name: '{full_name}' | Email: '{email}'")

        # 1. Validation: Required fields
        if not email.strip() or not password.strip():
            flash("Email and password are required.", "warning")
            return render_template("register.html")

        # 2. Validation: Passwords match
        if confirm_password and password != confirm_password:
            flash("Passwords do not match.", "warning")
            print("FAILED: Password mismatch")
            return render_template("register.html")

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        try:
            # Dynamically match column names in the 'users' table
            columns = get_users_columns(conn)

            if "full_name" in columns:
                conn.execute("INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)", (full_name, email, hashed_pw))
            elif "name" in columns:
                conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (full_name, email, hashed_pw))
            elif "username" in columns:
                conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (full_name, email, hashed_pw))
            else:
                conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))

            conn.commit()
            print("SUCCESS: Account created! Redirecting to login...\n")
            flash("Account created! Please log in.", "success")
            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError as e:
            print(f"FAILED: DB IntegrityError - {e}\n")
            flash("That email is already registered. Try logging in instead.", "warning")
        except Exception as e:
            print(f"FAILED: Unexpected Error - {e}\n")
            flash(f"Error creating account: {e}", "danger")
        finally:
            conn.close()

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))