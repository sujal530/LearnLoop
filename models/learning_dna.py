"""
models/learning_dna.py

Learning DNA model for LearnLoop AI
"""

from dataclasses import dataclass


@dataclass
class LearningDNA:
    user_id: int
    consistency: int = 0
    confidence: int = 0
    understanding: int = 0
    quiz_score: int = 0
    study_hours: int = 0

    def calculate_score(self):
        """
        Calculate the overall Learning DNA score.
        """

        score = (
            self.consistency +
            self.confidence +
            self.understanding +
            self.quiz_score +
            self.study_hours
        ) / 5

        return round(score)

    def get_level(self):
        """
        Return learner level based on DNA score.
        """

        score = self.calculate_score()

        if score >= 90:
            return "Master"

        elif score >= 75:
            return "Advanced"

        elif score >= 60:
            return "Intermediate"

        elif score >= 40:
            return "Beginner"

        return "Starter"

    def to_dict(self):
        """
        Convert model to dictionary.
        """

        return {
            "user_id": self.user_id,
            "consistency": self.consistency,
            "confidence": self.confidence,
            "understanding": self.understanding,
            "quiz_score": self.quiz_score,
            "study_hours": self.study_hours,
            "learning_dna": self.calculate_score(),
            "level": self.get_level()
        }
        