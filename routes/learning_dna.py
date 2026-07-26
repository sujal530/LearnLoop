"""
Learning DNA Module
LearnLoop AI

Calculates the learner's Learning DNA score based on
study habits and performance.
"""


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

    # -------------------------
    # Consistency Score
    # -------------------------
    def consistency_score(self):

        if self.consistency >= 30:
            return 100
        elif self.consistency >= 20:
            return 80
        elif self.consistency >= 10:
            return 60
        else:
            return 40

    # -------------------------
    # Confidence Score
    # -------------------------
    def confidence_score(self):
        return min(self.confidence, 100)

    # -------------------------
    # Understanding Score
    # -------------------------
    def understanding_score(self):
        return min(self.understanding, 100)

    # -------------------------
    # Quiz Score
    # -------------------------
    def quiz_performance(self):
        return min(self.quiz_score, 100)

    # -------------------------
    # Study Hours Score
    # -------------------------
    def study_score(self):

        if self.study_hours >= 4:
            return 100
        elif self.study_hours >= 3:
            return 80
        elif self.study_hours >= 2:
            return 60
        else:
            return 40

    # -------------------------
    # Final Learning DNA
    # -------------------------
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

    # -------------------------
    # DNA Level
    # -------------------------
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


# ----------------------------------
# Example
# ----------------------------------
if __name__ == "__main__":

    dna = LearningDNA(
        consistency=25,
        confidence=80,
        understanding=85,
        quiz_score=90,
        study_hours=3
    )

    print(dna.calculate())
    