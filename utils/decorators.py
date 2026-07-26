"""
decorators.py
Reusable decorators for LearnLoop AI
"""

from functools import wraps
from flask import session, redirect, url_for, flash


# ---------------------------------
# Login Required
# ---------------------------------
def login_required(func):
    """
    Allows access only to logged-in users.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


# ---------------------------------
# Guest Only
# ---------------------------------
def guest_only(func):
    """
    Prevent logged-in users from accessing
    login/register pages.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" in session:
            return redirect(url_for("dashboard.dashboard"))

        return func(*args, **kwargs)

    return wrapper


# ---------------------------------
# Admin Required (Future Use)
# ---------------------------------
def admin_required(func):
    """
    Allows only admin users.
    Requires 'role' in session.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            flash("Access Denied.", "danger")
            return redirect(url_for("dashboard.dashboard"))

        return func(*args, **kwargs)

    return wrapper
