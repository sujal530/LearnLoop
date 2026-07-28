"""
models/task.py

Task model for LearnLoop AI
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int = None
    user_id: int = 0
    roadmap_id: int = 0

    title: str = ""
    description: str = ""

    category: str = "Learning"
    priority: str = "Medium"
    estimated_time: int = 60      # Minutes

    status: str = "pending"       # 'pending', 'in_progress', or 'completed'
    due_date: str = ""

    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    @property
    def completed(self) -> bool:
        return self.status == "completed"

    def mark_completed(self):
        self.status = "completed"

    def mark_pending(self):
        self.status = "pending"

    def priority_color(self):
        colors = {
            "Low": "success",
            "Medium": "warning",
            "High": "danger"
        }
        return colors.get(self.priority, "secondary")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "roadmap_id": self.roadmap_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "estimated_time": self.estimated_time,
            "status": self.status,
            "completed": self.completed,
            "due_date": self.due_date,
            "created_at": self.created_at
        }