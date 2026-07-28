import os
import logging
from google import genai
from config import Config

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            print("❌ GEMINI_API_KEY not found")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
                print("✅ Gemini Client Initialized")
            except Exception as e:
                print("Gemini Initialization Error:", e)
                self.client = None

    def mentor_chat(self, message, history=None):
        if not self.client:
            return "Gemini client is not initialized."

        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=message
            )

            return response.text

        except Exception as e:
            print("AI Mentor Error:", e)
            return f"Error: {e}"

    def generate_quiz(self, topic, difficulty="Beginner"):
    
        prompt = f"""
You are an expert quiz generator.

Create exactly 5 multiple choice questions.

Topic:
{topic}

Difficulty:
{difficulty}

Return EXACTLY in this format.

Question 1:
What is Python?
A. Programming Language
B. Database
C. Browser
D. Operating System
Answer: A

Question 2:
...

Do not use markdown.

Do not write explanations.

Do not write anything except the quiz.
"""

        return self.mentor_chat(prompt)

    def generate_roadmap(self, goal, level, study_time, deadline):
        prompt = f"""
Create a detailed learning roadmap.

Goal: {goal}
Level: {level}
Study Time: {study_time} hours/day
Deadline: {deadline}
"""

        return self.mentor_chat(prompt)


ai_service = AIService()