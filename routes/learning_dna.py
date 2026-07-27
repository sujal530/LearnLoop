"""
Learning DNA Route & Module
LearnLoop AI
"""

from flask import Blueprint, render_template, request, jsonify, session
from utils.decorators import login_required


# 1. Define the Blueprint that app.py is looking for
learning_dna_bp = Blueprint("learning_dna", __name__)


# 2. Your LearningDNA Calculation Logic
class LearningDNA:
    def __init__(
        self,
        consistency,
        confidence,
        understanding,
        quiz_score,
        study_hours
    ):
        self.consistency = consistency
        self.confidence = confidence
        self.understanding = understanding
        self.quiz_score = quiz_score
        self.study_hours = study_hours

    def consistency_score(self):
        if self.consistency >= 30:
            return 100
        elif self.consistency >= 20:
            return 80
        elif self.consistency >= 10:
            return 60
        else:
            return 40

    def confidence_score(self):
        return min(self.confidence, 100)

    def understanding_score(self):
        return min(self.understanding, 100)

    def quiz_performance(self):
        return min(self.quiz_score, 100)

    def study_score(self):
        if self.study_hours >= 4:
            return 100
        elif self.study_hours >= 3:
            return 80
        elif self.study_hours >= 2:
            return 60
        else:
            return 40

    def calculate(self):
        total = (
            self.consistency_score()
            + self.confidence_score()
            + self.understanding_score()
            + self.quiz_performance()
            + self.study_score()
        )

        dna = round(total / 5)

        return {
            "Learning DNA": dna,
            "Consistency": self.consistency_score(),
            "Confidence": self.confidence_score(),
            "Understanding": self.understanding_score(),
            "Quiz": self.quiz_performance(),
            "Study Hours": self.study_score(),
            "Level": self.level(dna)
        }

    def level(self, score):
        if score >= 90:
            return "Master"
        elif score >= 75:
            return "Advanced"
        elif score >= 60:
            return "Intermediate"
        elif score >= 40:
            return "Beginner"
        return "Starter"


# 3. Add your Flask Route(s)
@learning_dna_bp.route("/learning-dna", methods=["GET"])
@login_required
def view_learning_dna():
    # Example stats (you can pull real numbers from your SQLite DB later)
    dna_calculator = LearningDNA(
        consistency=25,
        confidence=80,
        understanding=85,
        quiz_score=90,
        study_hours=3
    )
    results = dna_calculator.calculate()
    
    return render_template("learning_dna.html", dna=results)