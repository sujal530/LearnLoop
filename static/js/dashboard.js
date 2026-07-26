/**
 * dashboard.js
 * -----------------------------------------------------------------------
 * Populates #dashboard-container: summary stats, the upcoming tasks list,
 * and the charts defined in charts.js.
 *
 * DEPENDS ON (must load before this file):
 *   - script.js  -> fetchJson(), getEmbeddedData()
 *   - charts.js  -> initDashboardCharts()
 *
 * DATA SOURCE
 * Tries embedded JSON first (<script type="application/json" id="dashboard-data">
 * rendered by Flask/Jinja on GET /dashboard), then falls back to fetching
 * /progress and /tasks directly. This avoids requiring a new API route.
 *
 * SCOPE NOTE: "streak" and "study hours" appear in the pitch deck, but need a
 * per-day activity log that isn't in the current schema (Progress only has
 * topic/completion, Tasks only has status/deadline — no completed_at date).
 * Those two are left out rather than faked; everything below is computed
 * from real Progress/Tasks columns.
 *
 * IDS ADDED OUT OF NECESSITY (not in the shared id list, which has no ids
 * for dashboard stat widgets): overall-completion-value, upcoming-tasks-count,
 * upcoming-tasks-list. All three must exist inside #dashboard-container.
 */

async function loadDashboardData() {
    const embeddedData = getEmbeddedData('dashboard-data');
    if (embeddedData) {
        return embeddedData;
    }

    try {
        const [progressData, taskData] = await Promise.all([
            fetchJson('/progress'),
            fetchJson('/tasks')
        ]);
        return { progress: progressData || [], tasks: taskData || [], weeklyActivity: [] };
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        return { progress: [], tasks: [], weeklyActivity: [] };
    }
}

/**
 * Computes the overall completion percentage across all topics.
 * @param {Array<{completion: number}>} progressData
 */
function calculateOverallCompletion(progressData) {
    if (!Array.isArray(progressData) || progressData.length === 0) {
        return 0;
    }

    const totalCompletion = progressData.reduce((sum, entry) => sum + (entry.completion || 0), 0);
    return Math.round(totalCompletion / progressData.length);
}

/**
 * Renders the small summary stat cards inside #dashboard-container.
 */
function renderSummaryStats(dashboardData) {
    const overallCompletionElement = document.getElementById('overall-completion-value');
    const upcomingTasksCountElement = document.getElementById('upcoming-tasks-count');

    const overallCompletion = calculateOverallCompletion(dashboardData.progress);
    const upcomingTasks = (dashboardData.tasks || []).filter((task) => task.status !== 'completed');

    if (overallCompletionElement) {
        overallCompletionElement.textContent = `${overallCompletion}%`;
    }

    if (upcomingTasksCountElement) {
        upcomingTasksCountElement.textContent = String(upcomingTasks.length);
    }
}

/**
 * Renders the upcoming tasks list, soonest deadline first.
 * @param {Array<{title: string, status: string, deadline: string}>} taskData
 */
function renderUpcomingTasksList(taskData) {
    const upcomingTasksList = document.getElementById('upcoming-tasks-list');
    if (!upcomingTasksList) {
        return;
    }

    const upcomingTasks = (taskData || [])
        .filter((task) => task.status !== 'completed')
        .sort((firstTask, secondTask) => new Date(firstTask.deadline) - new Date(secondTask.deadline));

    upcomingTasksList.innerHTML = '';

    if (upcomingTasks.length === 0) {
        const emptyStateItem = document.createElement('li');
        emptyStateItem.className = 'task-item task-item-empty';
        emptyStateItem.textContent = 'No upcoming tasks. You are all caught up!';
        upcomingTasksList.appendChild(emptyStateItem);
        return;
    }

    upcomingTasks.forEach((task) => {
        const taskItem = document.createElement('li');
        taskItem.className = 'task-item';

        const taskTitle = document.createElement('span');
        taskTitle.className = 'task-item-title';
        taskTitle.textContent = task.title;

        const taskDeadline = document.createElement('span');
        taskDeadline.className = 'task-item-deadline';
        taskDeadline.textContent = task.deadline
            ? new Date(task.deadline).toLocaleDateString()
            : 'No deadline';

        taskItem.appendChild(taskTitle);
        taskItem.appendChild(taskDeadline);
        upcomingTasksList.appendChild(taskItem);
    });
}

async function initDashboardPage() {
    const dashboardContainer = document.getElementById('dashboard-container');
    if (!dashboardContainer) {
        return;
    }

    const dashboardData = await loadDashboardData();

    renderSummaryStats(dashboardData);
    renderUpcomingTasksList(dashboardData.tasks);

    if (typeof initDashboardCharts === 'function') {
        initDashboardCharts(dashboardData);
    }
}

document.addEventListener('DOMContentLoaded', initDashboardPage);