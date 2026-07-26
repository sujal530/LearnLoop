"""
models/roadmap.py

Roadmap model for LearnLoop AI
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Roadmap:
    user_id: int
    goal: str
    skill_level: str
    study_hours_per_day: int
    duration_weeks: int
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    weekly_plan: list = field(default_factory=list)

    # ---------------------------------
    # Add Weekly Plan
    # ---------------------------------
    def add_week(self, title, topics):
        """
        Add a weekly learning plan.
        """

        self.weekly_plan.append({
            "week": len(self.weekly_plan) + 1,
            "title": title,
            "topics": topics
        })

    # ---------------------------------
    # Total Weeks
    # ---------------------------------
    def total_weeks(self):
        return len(self.weekly_plan)

    # ---------------------------------
    # Get Specific Week
    # ---------------------------------
    def get_week(self, week_number):

        if 1 <= week_number <= len(self.weekly_plan):
            return self.weekly_plan[week_number - 1]

        return None

    # ---------------------------------
    # Completion Percentage
    # ---------------------------------
    def completion_percentage(self, completed_weeks):

        if self.duration_weeks == 0:
            return 0

        return round(
            (completed_weeks / self.duration_weeks) * 100,
            2
        )

    # ---------------------------------
    # Convert to Dictionary
    # ---------------------------------
    def to_dict(self):

        return {
            "user_id": self.user_id,
            "goal": self.goal,
            "skill_level": self.skill_level,
            "study_hours_per_day": self.study_hours_per_day,
            "duration_weeks": self.duration_weeks,
            "created_at": self.created_at,
            "weekly_plan": self.weekly_plan
        }
        