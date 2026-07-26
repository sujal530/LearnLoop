"""
models/quiz.py

Quiz model for LearnLoop AI
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Quiz:
    user_id: int
    topic: str
    score: int = 0
    total_questions: int = 5
    difficulty: str = "Beginner"
    completed_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def percentage(self):
        """
        Calculate quiz percentage.
        """

        if self.total_questions == 0:
            return 0

        return round(
            (self.score / self.total_questions) * 100,
            2
        )

    def is_passed(self):
        """
        Return True if learner passed.
        """

        return self.percentage() >= 70

    def grade(self):
        """
        Return grade.
        """

        percent = self.percentage()

        if percent >= 90:
            return "A+"

        elif percent >= 80:
            return "A"

        elif percent >= 70:
            return "B"

        elif percent >= 60:
            return "C"

        elif percent >= 50:
            return "D"

        return "F"

    def feedback(self):
        """
        Return learner feedback.
        """

        percent = self.percentage()

        if percent >= 90:
            return "Excellent work! Keep it up."

        elif percent >= 80:
            return "Very good performance."

        elif percent >= 70:
            return "Good job. Keep practicing."

        elif percent >= 60:
            return "Needs some revision."

        return "More practice is recommended."

    def to_dict(self):
        """
        Convert object into dictionary.
        """

        return {
            "user_id": self.user_id,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "score": self.score,
            "total_questions": self.total_questions,
            "percentage": self.percentage(),
            "grade": self.grade(),
            "passed": self.is_passed(),
            "feedback": self.feedback(),
            "completed_at": self.completed_at
        }
        