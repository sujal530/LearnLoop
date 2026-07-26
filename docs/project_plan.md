# LearnLoop AI - Project Plan

## Project Title

**LearnLoop AI – Your AI Mentor That Learns With You**

---

# Team

**Team Name:** Error404

### Members

- Sujal Jadhav (Leader)
- Ankush
- Rohit
- Kunal

---

# Problem Statement

Modern learning platforms mainly recommend content instead of actively mentoring learners. As a result, students often face:

- Information overload
- Lack of personalized guidance
- Static learning paths
- Poor accountability
- Low completion rates

LearnLoop AI addresses these challenges by acting as an AI-powered mentor that creates adaptive learning plans, provides guidance, and continuously adjusts the learner's journey.

---

# Project Objective

Develop an AI-powered web application that:

- Understands learner goals
- Creates personalized learning roadmaps
- Generates daily study tasks
- Provides AI mentoring
- Tracks learning progress
- Measures Learning DNA
- Adapts future learning plans based on performance

---

# Core Features

## Phase 1 – Authentication

- User Registration
- Login
- Logout
- Session Management

---

## Phase 2 – Goal Intake

Collect:

- Learning Goal
- Skill Level
- Daily Study Hours
- Deadline

Output:

- Personalized learner profile

---

## Phase 3 – AI Roadmap

Generate:

- Weekly roadmap
- Topic sequence
- Milestones
- Study schedule

---

## Phase 4 – Daily Tasks

Break weekly plans into daily tasks.

Each task contains:

- Topic
- Estimated study time
- Priority
- Completion status

---

## Phase 5 – AI Mentor

Google Gemini provides:

- Doubt solving
- Concept explanation
- Study guidance
- Quiz generation
- Learning suggestions

---

## Phase 6 – Quiz System

Generate quizzes based on:

- Current roadmap
- Completed topics
- Difficulty level

Track:

- Score
- Percentage
- Weak topics

---

## Phase 7 – Progress Dashboard

Track:

- Completed Tasks
- Total Tasks
- Study Hours
- Learning Streak
- Weekly Progress
- Completion Percentage

---

## Phase 8 – Learning DNA

Evaluate learners using:

- Consistency
- Confidence
- Understanding
- Quiz Performance
- Study Hours

Generate an overall Learning DNA score.

---

## Phase 9 – Feedback Loop

Update future learning plans based on:

- Quiz results
- Missed tasks
- Weak areas
- User progress

---

# System Architecture

Frontend

- HTML5
- CSS3
- JavaScript

↓

Backend

- Flask

↓

AI Engine

- Google Gemini API

↓

Database

- SQLite

↓

Analytics

- Chart.js

---

# Folder Structure

```
LearnLoopAI/

│
├── app.py
├── config.py
├── requirements.txt
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── mentor.py
│   ├── profile.py
│   ├── progress.py
│   ├── quiz.py
│   ├── roadmap.py
│   └── tasks.py
│
├── models/
│   ├── user.py
│   ├── roadmap.py
│   ├── task.py
│   ├── quiz.py
│   ├── progress.py
│   └── learning_dna.py
│
├── utils/
│   ├── auth.py
│   ├── database.py
│   ├── decorators.py
│   ├── gemini.py
│   ├── helpers.py
│   ├── learning_dna.py
│   └── validators.py
│
├── templates/
│
├── static/
│
├── docs/
│
└── tests/
```

---

# Development Timeline

### Stage 1

- Project setup
- Folder structure
- Database

### Stage 2

- Authentication
- Dashboard

### Stage 3

- Goal Intake
- AI Roadmap

### Stage 4

- Daily Tasks

### Stage 5

- AI Mentor

### Stage 6

- Quiz Module

### Stage 7

- Progress Dashboard

### Stage 8

- Learning DNA

### Stage 9

- Feedback Loop

### Stage 10

- Testing
- Bug Fixes
- Deployment

---

# Technology Stack

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- Flask

AI

- Google Gemini API

Database

- SQLite

Charts

- Chart.js

Version Control

- Git
- GitHub

---

# Future Enhancements

- Voice AI Mentor
- Flutter Mobile App
- Resume Builder
- Interview Preparation
- AI Career Guidance
- Gamification
- Cloud Sync
- Multi-language Support

---

# Success Criteria

The project is considered successful if it can:

- Register and authenticate users
- Generate personalized learning roadmaps
- Create daily study tasks
- Answer learner questions using AI
- Generate quizzes
- Track learner progress
- Calculate Learning DNA
- Adapt learning plans based on user performance

---

# Project Status

Current Version:

**LearnLoop AI v1.0**

Status:

**Under Development**