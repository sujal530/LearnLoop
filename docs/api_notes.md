# LearnLoop AI API Documentation

## Overview

LearnLoop AI provides REST APIs for authentication, AI mentoring, roadmap generation, quizzes, progress tracking, and user profile management.

**Base URL**

```
http://127.0.0.1:5000
```

---

# Authentication

## Register

**Endpoint**

```
POST /register
```

### Request

```json
{
    "name": "Ankush",
    "email": "ankush@example.com",
    "password": "Password123"
}
```

### Response

```json
{
    "message": "Registration Successful"
}
```

---

## Login

**Endpoint**

```
POST /login
```

### Request

```json
{
    "email": "ankush@example.com",
    "password": "Password123"
}
```

### Response

```json
{
    "message": "Login Successful"
}
```

---

## Logout

**Endpoint**

```
GET /logout
```

---

# Dashboard

## Get Dashboard

**Endpoint**

```
GET /dashboard
```

### Returns

- User Information
- Goal
- Progress
- Streak
- Study Hours

---

# Goal Intake

## Create Goal

**Endpoint**

```
POST /roadmap
```

### Request

```json
{
    "goal": "Become Python Developer",
    "level": "Beginner",
    "study_time": 2,
    "deadline": "2026-09-30"
}
```

---

# AI Mentor

## Chat

**Endpoint**

```
POST /mentor/chat
```

### Request

```json
{
    "message": "Explain Python Loops."
}
```

### Response

```json
{
    "response": "Python loops allow..."
}
```

---

## Generate Roadmap

**Endpoint**

```
POST /mentor/roadmap
```

### Request

```json
{
    "goal": "Learn Flask",
    "level": "Intermediate",
    "study_time": 3
}
```

---

## Generate Quiz

**Endpoint**

```
POST /mentor/quiz
```

### Request

```json
{
    "topic": "Python"
}
```

---

# Quiz

## Generate Quiz

**Endpoint**

```
POST /quiz/generate
```

### Request

```json
{
    "topic": "Flask",
    "difficulty": "Intermediate"
}
```

---

## Submit Quiz

**Endpoint**

```
POST /quiz/submit
```

### Request

```json
{
    "score": 4,
    "total": 5
}
```

### Response

```json
{
    "percentage": 80,
    "message": "Quiz Submitted Successfully"
}
```

---

## Quiz History

**Endpoint**

```
GET /quiz/history
```

---

# Tasks

## Get Tasks

**Endpoint**

```
GET /tasks
```

---

## Add Task

**Endpoint**

```
POST /tasks/add
```

---

## Complete Task

**Endpoint**

```
POST /tasks/complete
```

---

# Progress

## View Progress

**Endpoint**

```
GET /progress
```

---

## Update Progress

**Endpoint**

```
POST /progress/update
```

### Request

```json
{
    "completed_tasks": 12,
    "total_tasks": 20,
    "study_hours": 35,
    "streak": 7
}
```

---

## Progress API

**Endpoint**

```
GET /api/progress
```

### Example Response

```json
{
    "completed_tasks": 12,
    "total_tasks": 20,
    "study_hours": 35,
    "streak": 7,
    "completion": 60
}
```

---

# Learning DNA

## View Learning DNA

**Endpoint**

```
GET /learning_dna
```

### Response

```json
{
    "consistency": 82,
    "confidence": 78,
    "understanding": 91,
    "quiz_score": 85,
    "study_hours": 88,
    "learning_dna": 85
}
```

---

# Profile

## Get Profile

**Endpoint**

```
GET /profile
```

---

## Update Profile

**Endpoint**

```
POST /profile/edit
```

---

## Change Password

**Endpoint**

```
POST /profile/password
```

---

# Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

---

# Authentication

Protected endpoints require an authenticated user session.

Examples:

- `/dashboard`
- `/mentor`
- `/quiz`
- `/roadmap`
- `/tasks`
- `/progress`
- `/profile`

---

# Technology Stack

- Flask
- Python
- SQLite
- Google Gemini API
- HTML
- CSS
- JavaScript
- Chart.js

---

# Version

**LearnLoop AI API v1.0**