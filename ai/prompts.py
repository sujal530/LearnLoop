"""
ai/prompts.py

Central prompt library for LearnLoop AI
"""


# -----------------------------------------
# System Prompt
# -----------------------------------------

SYSTEM_PROMPT = """
You are LearnLoop AI.

You are an AI Learning Mentor.

Your responsibilities:

- Teach concepts clearly.
- Create learning roadmaps.
- Generate quizzes.
- Answer doubts.
- Motivate learners.
- Adapt responses to the learner's level.

Always explain in simple language.
"""


# -----------------------------------------
# Explain Topic
# -----------------------------------------

def explain_prompt(topic):

    return f"""
{SYSTEM_PROMPT}

Explain the following topic.

Topic:
{topic}

Instructions:

- Beginner friendly
- Step-by-step
- Give examples
- Highlight important concepts
- End with a short summary
"""


# -----------------------------------------
# Roadmap Prompt
# -----------------------------------------

def roadmap_prompt(
    goal,
    level,
    study_hours,
    deadline
):

    return f"""
{SYSTEM_PROMPT}

Create a personalized learning roadmap.

Goal:
{goal}

Current Level:
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

Include:

- Topics
- Mini projects
- Revision
- Practice
"""


# -----------------------------------------
# Daily Tasks Prompt
# -----------------------------------------

def task_prompt(topic):

    return f"""
{SYSTEM_PROMPT}

Generate 5 daily learning tasks.

Topic:

{topic}

Each task should include:

- Title
- Description
- Estimated Time
"""


# -----------------------------------------
# Quiz Prompt
# -----------------------------------------

def quiz_prompt(
    topic,
    difficulty
):

    return f"""
{SYSTEM_PROMPT}

Generate 5 multiple-choice questions.

Topic:
{topic}

Difficulty:
{difficulty}

Return format:

Question

A.

B.

C.

D.

Correct Answer
"""


# -----------------------------------------
# Doubt Solver Prompt
# -----------------------------------------

def doubt_prompt(question):

    return f"""
{SYSTEM_PROMPT}

Answer this learner's question.

Question:

{question}

Instructions:

- Simple language
- Step-by-step
- Example
- Common mistakes
- Quick summary
"""


# -----------------------------------------
# Revision Notes Prompt
# -----------------------------------------

def revision_prompt(topic):

    return f"""
{SYSTEM_PROMPT}

Generate revision notes.

Topic:

{topic}

Include:

- Definitions
- Key Points
- Tips
- Important Facts
"""


# -----------------------------------------
# Learning DNA Prompt
# -----------------------------------------

def dna_prompt(
    consistency,
    confidence,
    understanding,
    quiz_score
):

    return f"""
Analyze the learner.

Consistency:
{consistency}

Confidence:
{confidence}

Understanding:
{understanding}

Quiz Performance:
{quiz_score}

Give:

- Strengths
- Weaknesses
- Study Suggestions
"""


# -----------------------------------------
# Motivation Prompt
# -----------------------------------------

def motivation_prompt(streak):

    return f"""
A learner has maintained a study streak of {streak} days.

Write a short motivational message.

Maximum 80 words.
"""


# -----------------------------------------
# Feedback Prompt
# -----------------------------------------

def feedback_prompt(score):

    return f"""
Quiz Score:

{score}%

Provide:

- Performance Analysis
- Weak Areas
- Revision Topics
- Next Learning Step
"""
