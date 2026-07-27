/**
 * dashboard.js
 * -----------------------------------------------------------------------
 * Populates #dashboard-container: summary stats, the upcoming tasks list,
 * and the charts defined in charts.js.
 */

// Safety Fallbacks for helper functions if script.js isn't loaded first
if (typeof getEmbeddedData !== 'function') {
    window.getEmbeddedData = function(id) {
        const scriptTag = document.getElementById(id);
        if (scriptTag && scriptTag.textContent) {
            try { 
                return JSON.parse(scriptTag.textContent); 
            } catch (e) { 
                return null; 
            }
        }
        return null;
    };
}

if (typeof fetchJson !== 'function') {
    window.fetchJson = async function(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) return null;
            return await response.json();
        } catch (e) {
            return null;
        }
    };
}

/**
 * Fetches dashboard data from embedded JSON script tag or falls back to APIs.
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
 * Renders the summary stat cards inside #dashboard-container.
 */
function renderSummaryStats(dashboardData) {
    const overallCompletionElement = document.getElementById('overall-completion-value');
    const upcomingTasksCountElement = document.getElementById('upcoming-tasks-count');

    const overallCompletion = calculateOverallCompletion(dashboardData.progress);
    const upcomingTasks = (dashboardData.tasks || []).filter((task) => task.status !== 'completed');

    if (overallCompletionElement && overallCompletion > 0) {
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
        .sort((firstTask, secondTask) => new Date(firstTask.deadline || 0) - new Date(secondTask.deadline || 0));

    // Only overwrite list if API returned tasks
    if (upcomingTasks.length > 0) {
        upcomingTasksList.innerHTML = '';
        upcomingTasks.forEach((task) => {
            const taskItem = document.createElement('li');
            taskItem.className = 'upcoming-task-item';

            const taskTitle = document.createElement('span');
            taskTitle.className = 'task-title';
            taskTitle.textContent = task.title;

            const taskDeadline = document.createElement('span');
            taskDeadline.className = 'task-due';
            taskDeadline.textContent = task.deadline
                ? new Date(task.deadline).toLocaleDateString()
                : 'No deadline';

            taskItem.appendChild(taskTitle);
            taskItem.appendChild(taskDeadline);
            upcomingTasksList.appendChild(taskItem);
        });
    }
}

/**
 * Initializes all dashboard components safely.
 */
async function initDashboardPage() {
    const dashboardContainer = document.getElementById('dashboard-container');
    if (!dashboardContainer) {
        return;
    }

    const dashboardData = await loadDashboardData();

    renderSummaryStats(dashboardData);
    renderUpcomingTasksList(dashboardData.tasks);

    // Safely execute chart drawing if Chart.js and helper are loaded
    if (typeof Chart !== 'undefined' && typeof initDashboardCharts === 'function') {
        try {
            initDashboardCharts(dashboardData);
        } catch (err) {
            console.error('Failed to initialize charts:', err);
        }
    } else {
        console.warn('Chart.js or initDashboardCharts function is not ready yet.');
    }
}

document.addEventListener('DOMContentLoaded', initDashboardPage);