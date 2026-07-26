from flask import Blueprint, render_template

roadmap_bp = Blueprint("roadmap", __name__)

@roadmap_bp.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")