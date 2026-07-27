from flask import Blueprint, render_template
from models.task import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
def tasks():
    # TODO: Get current user (implement based on your auth system)
    # user_id = session.get('user_id')  # or similar
    
    # Fetch all tasks for the user from database
    # user_tasks = db.query(Task).filter_by(user_id=user_id).all()
    
    # For now, return empty list
    user_tasks = []
    
    return render_template("tasks.html", tasks=user_tasks)
