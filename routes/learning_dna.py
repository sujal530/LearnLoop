from flask import Blueprint, render_template
from models.learning_dna import LearningDNA

learning_dna_bp = Blueprint(
    "learning_dna",
    __name__,
    url_prefix="/learning-dna"
)

@learning_dna_bp.route("/")
def learning_dna():

    dna = LearningDNA(
        consistency=25,
        confidence=80,
        understanding=90,
        quiz_score=85,
        study_hours=3
    )

    return render_template(
        "learning_dna.html",
        result=dna.calculate()
    )