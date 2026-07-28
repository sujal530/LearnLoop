import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import Config
from models.task import Task

tasks_bp = Blueprint("tasks", __name__)


def get_db():
    conn = sqlite3.connect(Config.DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


@tasks_bp.route("/tasks", methods=["GET", "POST"])
def tasks():
    # 1. Fallback for testing/auth session
    user_id = session.get("user_id", 1)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "Learning").strip() or "Learning"
        priority = request.form.get("priority", "Medium")
        status = request.form.get("status", "pending")
        due_date = request.form.get("due_date", "")

        if not title:
            flash("Task title is required!", "danger")
            return redirect(url_for("tasks.tasks"))

        # Create Task instance
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=status,
            due_date=due_date
        )

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (user_id, title, description, category, priority, status, due_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    new_task.user_id,
                    new_task.title,
                    new_task.description,
                    new_task.category,
                    new_task.priority,
                    new_task.status,
                    new_task.due_date,
                    new_task.created_at
                )
            )
            conn.commit()
            conn.close()
            print(f"✅ TASK SAVED: '{new_task.title}'")
            flash("Task saved successfully!", "success")
        except sqlite3.Error as e:
            print(f"❌ DATABASE INSERT ERROR: {e}")
            flash(f"Database error: {e}", "danger")

        return redirect(url_for("tasks.tasks"))

    # Fetch tasks
    conn = get_db()
    raw_tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC", 
        (user_id,)
    ).fetchall()
    conn.close()

    # Instantiate Task objects so both dict-access and attributes work seamlessly
    tasks_list = []
    for row in raw_tasks:
        row_dict = dict(row)
        # Filter out keys that don't belong directly to the dataclass fields if needed
        task_obj = Task(
            id=row_dict.get("id"),
            user_id=row_dict.get("user_id", user_id),
            roadmap_id=row_dict.get("roadmap_id", 0),
            title=row_dict.get("title", ""),
            description=row_dict.get("description", ""),
            category=row_dict.get("category", "Learning"),
            priority=row_dict.get("priority", "Medium"),
            estimated_time=row_dict.get("estimated_time", 60),
            status=str(row_dict.get("status", "pending")).lower(),
            due_date=row_dict.get("due_date", ""),
            created_at=row_dict.get("created_at", "")
        )
        tasks_list.append(task_obj)

    return render_template("tasks.html", tasks=tasks_list)