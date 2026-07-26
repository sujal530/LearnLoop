from functools import wraps
from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------------------------------
# Password Helpers
# ---------------------------------------

def hash_password(password):
    """
    Hash a plain-text password before storing it.
    """
    return generate_password_hash(password)


def verify_password(hashed_password, password):
    """
    Verify a password against its hash.
    """
    return check_password_hash(hashed_password, password)


# ---------------------------------------
# Login Helpers
# ---------------------------------------

def login_user(user):
    """
    Store user information in session.
    """
    session["user_id"] = user["id"]
    session["username"] = user["name"]


def logout_user():
    """
    Clear the current user session.
    """
    session.clear()


def is_logged_in():
    """
    Return True if a user is logged in.
    """
    return "user_id" in session


# ---------------------------------------
# Login Required Decorator
# ---------------------------------------

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view
