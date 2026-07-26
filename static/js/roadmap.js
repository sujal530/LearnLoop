/**
 * roadmap.js
 * -----------------------------------------------------------------------
 * Renders the learner's roadmap and daily task checklist inside
 * #roadmap-container.
 *
 * DEPENDS ON (must load before this file): script.js -> fetchJson(), getEmbeddedData(), showToast()
 *
 * DATA SOURCE: embedded JSON (<script type="application/json" id="roadmap-data">
 * rendered on GET /roadmap) with a GET /roadmap fallback. Expected shape:
 *   { roadmap: [{ id, title, description, difficulty }, ...],
 *     tasks:   [{ id, user_id, title, description, status, deadline }, ...] }
 *
 * SCOPE NOTE: Tasks has no column linking it back to a specific Roadmap row
 * (no roadmap_id/topic foreign key in the given schema), so this file does
 * NOT try to guess which tasks belong to which roadmap card — that would be
 * a fragile string match. Instead it renders two honest sections: the
 * roadmap itself, and the flat "Today's Tasks" checklist. Once models/ adds
 * a linking column, grouping can be added here in one place.
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
        showToast('Could not load your roadmap. Please try again.', 'error');
        return { roadmap: [], tasks: [] };
    }
}

/**
 * Builds one roadmap card.
 * @param {{title: string, description: string, difficulty: string}} roadmapItem
 */
function buildRoadmapCard(roadmapItem) {
    const roadmapCard = document.createElement('div');
    roadmapCard.className = 'roadmap-card';

    const cardTitle = document.createElement('h3');
    cardTitle.className = 'roadmap-card-title';
    cardTitle.textContent = roadmapItem.title;

    const difficultyBadge = document.createElement('span');
    difficultyBadge.className = `roadmap-card-difficulty roadmap-card-difficulty-${(roadmapItem.difficulty || '').toLowerCase()}`;
    difficultyBadge.textContent = roadmapItem.difficulty;

    const cardDescription = document.createElement('p');
    cardDescription.className = 'roadmap-card-description';
    cardDescription.textContent = roadmapItem.description;

    roadmapCard.appendChild(cardTitle);
    roadmapCard.appendChild(difficultyBadge);
    roadmapCard.appendChild(cardDescription);

    return roadmapCard;
}

/**
 * Builds one checklist row for a task, wired to toggle its status.
 * @param {{id: number, title: string, status: string}} task
 */
function buildTaskChecklistItem(task) {
    const taskItem = document.createElement('li');
    taskItem.className = 'roadmap-task-item';

    const taskCheckbox = document.createElement('input');
    taskCheckbox.type = 'checkbox';
    taskCheckbox.checked = task.status === 'completed';
    taskCheckbox.addEventListener('change', () => handleTaskStatusToggle(task.id, taskCheckbox.checked));

    const taskLabel = document.createElement('span');
    taskLabel.className = 'roadmap-task-label';
    taskLabel.textContent = task.title;

    taskItem.appendChild(taskCheckbox);
    taskItem.appendChild(taskLabel);
    return taskItem;
}

/**
 * Renders the roadmap section and the daily task checklist section.
 */
function renderRoadmap(roadmapData) {
    const roadmapContainer = document.getElementById('roadmap-container');
    if (!roadmapContainer) {
        return;
    }

    const roadmapItems = roadmapData.roadmap || [];
    const dailyTasks = roadmapData.tasks || [];

    roadmapContainer.innerHTML = '';

    const roadmapSection = document.createElement('div');
    roadmapSection.className = 'roadmap-section';

    const roadmapHeading = document.createElement('h2');
    roadmapHeading.textContent = 'Your Learning Roadmap';
    roadmapSection.appendChild(roadmapHeading);

    if (roadmapItems.length === 0) {
        const emptyMessage = document.createElement('p');
        emptyMessage.className = 'roadmap-empty-state';
        emptyMessage.textContent = 'Your roadmap has not been generated yet.';
        roadmapSection.appendChild(emptyMessage);
    } else {
        roadmapItems.forEach((roadmapItem) => {
            roadmapSection.appendChild(buildRoadmapCard(roadmapItem));
        });
    }

    const taskSection = document.createElement('div');
    taskSection.className = 'roadmap-task-section';

    const taskHeading = document.createElement('h2');
    taskHeading.textContent = "Today's Tasks";
    taskSection.appendChild(taskHeading);

    const taskList = document.createElement('ul');
    taskList.className = 'roadmap-task-list';

    if (dailyTasks.length === 0) {
        const emptyTaskItem = document.createElement('li');
        emptyTaskItem.className = 'roadmap-task-item-empty';
        emptyTaskItem.textContent = 'No tasks scheduled yet.';
        taskList.appendChild(emptyTaskItem);
    } else {
        dailyTasks.forEach((task) => taskList.appendChild(buildTaskChecklistItem(task)));
    }

    taskSection.appendChild(taskList);

    roadmapContainer.appendChild(roadmapSection);
    roadmapContainer.appendChild(taskSection);
}

/**
 * Persists a task completion toggle back to the backend.
 * @param {number} taskId
 * @param {boolean} isCompleted
 */
async function handleTaskStatusToggle(taskId, isCompleted) {
    try {
        await fetchJson('/tasks', {
            method: 'POST',
            body: { id: taskId, status: isCompleted ? 'completed' : 'pending' }
        });
        showToast(isCompleted ? 'Task marked complete!' : 'Task marked pending.', 'info');
    } catch (error) {
        console.error('Error updating task status:', error);
        showToast('Could not update task status.', 'error');
    }
}

async function initRoadmapPage() {
    const roadmapContainer = document.getElementById('roadmap-container');
    if (!roadmapContainer) {
        return;
    }

    const roadmapData = await loadRoadmapData();
    renderRoadmap(roadmapData);
}

document.addEventListener('DOMContentLoaded', initRoadmapPage);