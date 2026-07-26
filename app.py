from flask import Flask, render_template

from config import Config
from database.init_db import init_db

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

    with app.app_context():
        init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(learning_dna_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("500.html"), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)