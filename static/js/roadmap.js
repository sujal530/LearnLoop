/**
 * roadmap.js
 * -----------------------------------------------------------------------
 * Renders the learner's roadmap timeline and task list inside #roadmap-container.
 *
 * DEPENDS ON: script.js -> fetchJson(), getEmbeddedData(), showToast()
 */

async function loadRoadmapData() {
    const embeddedData = getEmbeddedData('roadmap-data');
    if (embeddedData) {
        return embeddedData;
    }

    try {
        const roadmapData = await fetchJson('/roadmap');
        return roadmapData || { roadmap: [], tasks: [] };
    } catch (error) {
        console.error('Error loading roadmap data:', error);
        if (typeof showToast === 'function') {
            showToast('Could not load your roadmap. Please try again.', 'error');
        }
        return { roadmap: [], tasks: [] };
    }
}

/**
 * Builds one roadmap card matching roadmap.css structure.
 */
function buildRoadmapCard(item, index) {
    const isCompleted = item.completion === 100;
    const isActive = item.completion > 0 && !isCompleted;
    const statusClass = isCompleted ? 'roadmap-node--completed' : (isActive ? 'roadmap-node--active' : '');
    const badgeSymbol = isCompleted ? '✓' : (index + 1);

    const link = document.createElement('a');
    link.href = item.id ? `/topic/${item.id}` : '#';
    link.className = `roadmap-node ${statusClass}`;

    const difficulty = (item.difficulty || 'beginner').toLowerCase();

    link.innerHTML = `
        <div class="roadmap-node-body">
            <div class="roadmap-node-head">
                <h3 class="roadmap-node-title">
                    <span class="node-index">${badgeSymbol}</span>
                    ${item.title || 'Untitled Topic'}
                </h3>
                <span class="difficulty-pill difficulty-${difficulty}">${item.difficulty || 'Beginner'}</span>
            </div>
            <p class="roadmap-node-description">${item.description || 'No description provided.'}</p>
            <div class="roadmap-node-meta">
                <div class="progress-bar">
                    <div class="progress-bar-fill" style="width: ${item.completion || 0}%;"></div>
                </div>
                <span class="progress-label">${item.completion || 0}% complete</span>
            </div>
        </div>
    `;

    return link;
}

/**
 * Builds one task checklist row matching roadmap.css.
 */
function buildTaskChecklistItem(task) {
    const taskItem = document.createElement('div');
    taskItem.className = `task-item ${task.status === 'completed' ? 'task-item--completed' : ''}`;

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'task-checkbox';
    checkbox.checked = task.status === 'completed';

    const titleSpan = document.createElement('span');
    titleSpan.className = 'task-title';
    titleSpan.textContent = task.title;

    checkbox.addEventListener('change', () => {
        const isChecked = checkbox.checked;
        taskItem.classList.toggle('task-item--completed', isChecked);
        handleTaskStatusToggle(task.id, isChecked);
    });

    taskItem.appendChild(checkbox);
    taskItem.appendChild(titleSpan);

    if (task.deadline || task.due_label) {
        const deadlineSpan = document.createElement('span');
        deadlineSpan.className = 'task-deadline';
        deadlineSpan.textContent = task.deadline || task.due_label;
        taskItem.appendChild(deadlineSpan);
    }

    return taskItem;
}

/**
 * Renders the page header, roadmap timeline, and daily tasks section.
 */
function renderRoadmap(roadmapData) {
    const roadmapContainer = document.getElementById('roadmap-container');
    if (!roadmapContainer) return;

    const roadmapItems = roadmapData.roadmap || [];
    const dailyTasks = roadmapData.tasks || [];

    roadmapContainer.innerHTML = '';

    // Header Section
    const headerDiv = document.createElement('div');
    headerDiv.className = 'roadmap-header';
    headerDiv.innerHTML = `
        <div>
            <h1 class="page-title">Your Learning Roadmap</h1>
            <p class="subtitle">A personalized path built around your goals.</p>
        </div>
        <div class="page-head-actions">
            <select class="select-input" id="roadmap-difficulty-filter">
                <option value="all">All difficulties</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
            </select>
        </div>
    `;
    roadmapContainer.appendChild(headerDiv);

    // Roadmap Timeline
    const timelineSection = document.createElement('section');
    timelineSection.className = 'roadmap-timeline';
    timelineSection.id = 'roadmap-track';

    if (roadmapItems.length === 0) {
        const emptyNode = document.createElement('div');
        emptyNode.className = 'roadmap-node';
        emptyNode.innerHTML = `<p class="roadmap-node-description">Your roadmap has not been generated yet.</p>`;
        timelineSection.appendChild(emptyNode);
    } else {
        roadmapItems.forEach((item, index) => {
            timelineSection.appendChild(buildRoadmapCard(item, index));
        });
    }
    roadmapContainer.appendChild(timelineSection);

    // Tasks Section
    if (dailyTasks.length > 0) {
        const taskSection = document.createElement('section');
        taskSection.style.marginTop = '2rem';
        
        const taskHeading = document.createElement('h2');
        taskHeading.style.marginBottom = '1rem';
        taskHeading.textContent = "Today's Tasks";
        taskSection.appendChild(taskHeading);

        const taskList = document.createElement('div');
        taskList.className = 'task-list';

        dailyTasks.forEach((task) => taskList.appendChild(buildTaskChecklistItem(task)));
        taskSection.appendChild(taskList);
        roadmapContainer.appendChild(taskSection);
    }
}

/**
 * Persists task completion toggle back to server.
 */
async function handleTaskStatusToggle(taskId, isCompleted) {
    try {
        const response = await fetch('/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id: taskId,
                status: isCompleted ? 'completed' : 'pending'
            })
        });

        if (!response.ok) throw new Error(`Server status ${response.status}`);

        if (typeof showToast === 'function') {
            showToast(isCompleted ? 'Task marked complete!' : 'Task marked pending.', 'info');
        }
    } catch (error) {
        console.error('Error updating task status:', error);
        if (typeof showToast === 'function') {
            showToast('Could not update task status.', 'error');
        }
    }
}

async function initRoadmapPage() {
    const roadmapContainer = document.getElementById('roadmap-container');
    if (!roadmapContainer) return;

    const roadmapData = await loadRoadmapData();
    renderRoadmap(roadmapData);
}

document.addEventListener('DOMContentLoaded', initRoadmapPage);