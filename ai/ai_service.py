"""
ai/ai_service.py

AI Service module handling integration with Google Gemini / Generative AI.
Provides fallback mock responses if GEMINI_API_KEY is not configured.
"""

import os
import logging
from config import Config

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.api_key = getattr(Config, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
        self.model = None

        if not self.api_key:
            logger.warning("GEMINI_API_KEY is missing. Running AIService in Fallback / Mock Mode.")
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-pro")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI model: {e}")
                self.model = None

    def generate_tasks(self, topic: str) -> list:
        """Generates a list of recommended daily study tasks for a given topic."""
        if self.model:
            try:
                prompt = f"Generate 3 concise, actionable learning tasks for studying '{topic}'. Return each task on a new line."
                response = self.model.generate_content(prompt)
                if response and response.text:
                    tasks = [line.strip("- ").strip() for line in response.text.strip().split("\n") if line.strip()]
                    return tasks[:5]
            except Exception as e:
                logger.error(f"AI Task Generation Error: {e}")

        # Fallback tasks if API key is missing or call fails
        return [
            f"Review fundamental concepts of {topic}",
            f"Complete practical exercises on {topic}",
            f"Summarize key takeaways for {topic}"
        ]

    def generate_roadmap(self, goal_title: str, target_weeks: int = 4) -> dict:
        """Generates a structured learning roadmap with weekly milestones."""
        if self.model:
            try:
                prompt = f"Create a {target_weeks}-week learning roadmap for '{goal_title}'. List 1 key milestone per week."
                response = self.model.generate_content(prompt)
                if response and response.text:
                    lines = [line.strip("- ").strip() for line in response.text.strip().split("\n") if line.strip()]
                    milestones = lines[:target_weeks]
                    return {
                        "title": goal_title,
                        "duration_weeks": target_weeks,
                        "milestones": milestones
                    }
            except Exception as e:
                logger.error(f"AI Roadmap Generation Error: {e}")

        # Fallback roadmap if API key is missing or call fails
        return {
            "title": goal_title,
            "duration_weeks": target_weeks,
            "milestones": [
                f"Week {i+1}: Fundamentals & Basics of {goal_title}" if i == 0 else f"Week {i+1}: Advanced Topics & Practice for {goal_title}"
                for i in range(target_weeks)
            ]
        }

    def ask_mentor(self, question: str) -> str:
        """Responds to user questions as an AI mentor."""
        if self.model:
            try:
                response = self.model.generate_content(question)
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.error(f"AI Mentor Error: {e}")

        return "I'm currently running in offline mode. Please configure your GEMINI_API_KEY to enable live AI responses!"


# Singleton instance
ai_service = AIService()