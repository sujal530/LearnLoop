"""
app.py

Main application factory and entry point for LearnLoop AI Flask application.
"""

import os
from flask import Flask, render_template, redirect, url_for, session, send_from_directory

from config import Config
from database.init_db import init_db

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.roadmap import roadmap_bp
from routes.tasks import tasks_bp
from routes.mentor import mentor_bp
from routes.quiz import quiz_bp
from routes.progress import progress_bp
from routes.profile import profile_bp
from routes.learning_dna import learning_dna_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable auto-reload for Jinja templates during development
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Ensure Upload Folder Exists
    upload_folder = os.path.join(app.root_path, "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    # Initialize Database Schema
    with app.app_context():
        init_db()

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(learning_dna_bp)

    # -------------------------------------------------------------
    # Global Context Processors & Template Helpers
    # -------------------------------------------------------------
    @app.context_processor
    def inject_user_context():
        """Makes session user info globally accessible across all Jinja templates."""
        return {
            "current_user_id": session.get("user_id"),
            "current_user_name": session.get("user_name", "Learner")
        }

    # -------------------------------------------------------------
    # Root Route
    # Directs users to Dashboard if logged in, or Login if not.
    # -------------------------------------------------------------
    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("dashboard.dashboard"))
        return redirect(url_for("auth.login"))

    # -------------------------------------------------------------
    # Uploads Route (for profile photos & task attachments)
    # -------------------------------------------------------------
    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        return send_from_directory(upload_folder, filename)

    # -------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        try:
            return render_template("500.html"), 500
        except Exception:
            return "<h1>500 - Internal Server Error</h1><p>Something went wrong on our end.</p>", 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)