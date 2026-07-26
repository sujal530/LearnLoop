"""
models/progress.py

Progress model for LearnLoop AI
"""

from dataclasses import dataclass


@dataclass
class Progress:
    user_id: int
    completed_tasks: int = 0
    total_tasks: int = 0
    study_hours: float = 0.0
    streak: int = 0

    def completion_percentage(self):
        """
        Calculate task completion percentage.
        """

        if self.total_tasks == 0:
            return 0

        return round(
            (self.completed_tasks / self.total_tasks) * 100,
            2
        )

    def add_completed_task(self):
        """
        Increase completed task count.
        """
        self.completed_tasks += 1

    def add_total_task(self):
        """
        Increase total task count.
        """
        self.total_tasks += 1

    def add_study_hours(self, hours):
        """
        Add study hours.
        """

        if hours > 0:
            self.study_hours += hours

    def increase_streak(self):
        """
        Increase learning streak.
        """
        self.streak += 1

    def reset_streak(self):
        """
        Reset learning streak.
        """
        self.streak = 0

    def to_dict(self):
        """
        Convert progress data into dictionary.
        """

        return {
            "user_id": self.user_id,
            "completed_tasks": self.completed_tasks,
            "total_tasks": self.total_tasks,
            "study_hours": self.study_hours,
            "streak": self.streak,
            "completion_percentage": self.completion_percentage()
        }
        