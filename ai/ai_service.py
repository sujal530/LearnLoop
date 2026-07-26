"""
ai/ai_service.py

Central AI service for LearnLoop AI
Handles all communication with Google Gemini.
"""

import google.generativeai as genai
from config import Config


class AIService:

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    # ---------------------------------------
    # Generate Generic AI Response
    # ---------------------------------------
    def ask(self, prompt: str):

        try:
            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"AI Error: {str(e)}"

    # ---------------------------------------
    # Explain Concept
    # ---------------------------------------
    def explain(self, topic: str):

        prompt = f"""
You are LearnLoop AI.

Explain the following topic in simple language.

Topic:
{topic}

Requirements:
- Beginner friendly
- Step-by-step
- Include one real-world example
"""

        return self.ask(prompt)

    # ---------------------------------------
    # Generate Weekly Roadmap
    # ---------------------------------------
    def generate_roadmap(
        self,
        goal,
        level,
        study_hours,
        deadline
    ):

        prompt = f"""
Create a personalized learning roadmap.

Goal:
{goal}

Skill Level:
{level}

Study Hours Per Day:
{study_hours}

Deadline:
{deadline}

Generate:

Week 1
Week 2
Week 3
...
until completion.
"""

        return self.ask(prompt)

    # ---------------------------------------
    # Generate Daily Tasks
    # ---------------------------------------
    def generate_tasks(self, topic):

        prompt = f"""
Generate 5 daily learning tasks.

Topic:
{topic}

Return tasks as a numbered list.
"""

        return self.ask(prompt)

    # ---------------------------------------
    # Generate Quiz
    # ---------------------------------------
    def generate_quiz(
        self,
        topic,
        difficulty="Beginner"
    ):

        prompt = f"""
Generate 5 multiple-choice questions.

Topic:
{topic}

Difficulty:
{difficulty}

Return:

Question

A.
B.
C.
D.

Answer:
"""

        return self.ask(prompt)

    # ---------------------------------------
    # Study Suggestions
    # ---------------------------------------
    def suggest_next_step(
        self,
        progress,
        weak_topics
    ):

        prompt = f"""
Student Progress:

Completion:
{progress}%

Weak Topics:
{weak_topics}

Suggest:

1. What to study next

2. Revision topics

3. Practice exercises
"""

        return self.ask(prompt)

    # ---------------------------------------
    # Motivation Message
    # ---------------------------------------
    def motivate(self, streak):

        prompt = f"""
Student has a learning streak of {streak} days.

Generate a short motivational message.
"""

        return self.ask(prompt)


# Singleton instance
ai_service = AIService()
