"""
ai/doubt_solver.py

AI Doubt Solver for LearnLoop AI
"""

from ai.ai_service import ai_service


class DoubtSolver:

    def __init__(self):
        self.ai = ai_service

    # ---------------------------------------
    # Solve Student Doubt
    # ---------------------------------------
    def solve(self, question: str):

        prompt = f"""
You are LearnLoop AI.

A student has asked the following question.

Question:
{question}

Instructions:

1. Explain in simple language.
2. Use step-by-step explanation.
3. Give one real-world example.
4. Mention common mistakes.
5. End with a quick summary.

Keep the answer beginner-friendly.
"""

        return self.ai.ask(prompt)

    # ---------------------------------------
    # Explain a Topic
    # ---------------------------------------
    def explain_topic(self, topic: str):

        prompt = f"""
Explain the topic:

{topic}

Requirements:

- Beginner friendly
- Easy language
- Step-by-step
- Include one example
- Mention important points
"""

        return self.ai.ask(prompt)

    # ---------------------------------------
    # Generate Practice Questions
    # ---------------------------------------
    def generate_practice(self, topic: str):

        prompt = f"""
Generate 5 practice questions on:

{topic}

Include:

- Short Answer Questions
- MCQs
- One Coding Question (if applicable)

Do not provide answers.
"""

        return self.ai.ask(prompt)

    # ---------------------------------------
    # Summarize Topic
    # ---------------------------------------
    def summarize(self, topic: str):

        prompt = f"""
Summarize the following topic:

{topic}

Maximum 10 bullet points.
"""

        return self.ai.ask(prompt)

    # ---------------------------------------
    # Generate Revision Notes
    # ---------------------------------------
    def revision_notes(self, topic: str):

        prompt = f"""
Create revision notes for:

{topic}

Include:

- Definitions
- Important formulas (if any)
- Key concepts
- Tips for remembering
"""

        return self.ai.ask(prompt)


# Singleton instance
doubt_solver = DoubtSolver()
