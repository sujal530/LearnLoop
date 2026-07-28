{% extends "base.html" %}

{% block title %}Tasks{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/tasks.css') }}">
{% endblock %}

{% block content %}
<div class="tasks-container" id="tasks-container">

  <!-- Header -->
  <div class="page-head">
    <div>
      <h1 class="page-title">Tasks</h1>
      <p class="page-subtitle">Everything you need to get done, in one place.</p>
    </div>
    <div class="page-head-actions">
      <button class="btn btn-primary" id="new-task-btn" type="button">+ New Task</button>
    </div>
  </div>

  <!-- Task Filters / Tabs -->
  <div class="task-tabs">
    <button class="task-tab-btn active" data-status="all">All</button>
    <button class="task-tab-btn" data-status="pending">Pending</button>
    <button class="task-tab-btn" data-status="in_progress">In Progress</button>
    <button class="task-tab-btn" data-status="completed">Completed</button>
  </div>

  <!-- Task Lists Container -->
  <div class="tasks-grid">
    <section class="task-group" data-status="pending">
      <h3 class="task-group-title">Pending</h3>
      <div class="task-list">
        {% for task in tasks if (task.status | lower) in ['pending', ''] %}
        <div class="task-card">
          <h4>{{ task.title }}</h4>
          <p>{{ task.description }}</p>
          {% if task.due_date %}<span class="task-date">📅 {{ task.due_date }}</span>{% endif %}
        </div>
        {% else %}
        <p class="empty-text">No pending tasks.</p>
        {% endfor %}
      </div>
    </section>

    <section class="task-group" data-status="in_progress">
      <h3 class="task-group-title">In Progress</h3>
      <div class="task-list">
        {% for task in tasks if (task.status | lower) == 'in_progress' %}
        <div class="task-card">
          <h4>{{ task.title }}</h4>
          <p>{{ task.description }}</p>
          {% if task.due_date %}<span class="task-date">📅 {{ task.due_date }}</span>{% endif %}
        </div>
        {% else %}
        <p class="empty-text">No tasks in progress.</p>
        {% endfor %}
      </div>
    </section>

    <section class="task-group" data-status="completed">
      <h3 class="task-group-title">Completed</h3>
      <div class="task-list">
        {% for task in tasks if (task.status | lower) == 'completed' %}
        <div class="task-card task-card-done">
          <h4>{{ task.title }}</h4>
          <p>{{ task.description }}</p>
          <span class="task-date">✓ Done</span>
        </div>
        {% else %}
        <p class="empty-text">No completed tasks yet.</p>
        {% endfor %}
      </div>
    </section>
  </div>

  <!-- Modal Overlay for Creating New Tasks -->
  <div class="modal-overlay" id="task-modal">
    <div class="modal-card">
      <h2>New Task</h2>
      <form action="{{ url_for('tasks.tasks') }}" method="POST" id="task-form">
        <div class="form-group">
          <label for="title">Title</label>
          <input type="text" id="title" name="title" class="form-control" placeholder="Task title" required>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" name="description" class="form-control" placeholder="Task description"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="deadline">Deadline</label>
            <input type="date" id="deadline" name="due_date" class="form-control">
          </div>
          <div class="form-group">
            <label for="status">Status</label>
            <select id="status" name="status" class="form-control">
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-outline" id="cancel-task-btn">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Task</button>
        </div>
      </form>
    </div>
  </div>

</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/tasks.js') }}"></script>
{% endblock %}