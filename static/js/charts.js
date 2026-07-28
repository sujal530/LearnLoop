/**
 * charts.js
 * -----------------------------------------------------------------------
 * Renders the analytics charts shown inside #dashboard-container.
 * Uses Chart.js (loaded via CDN <script> tag in templates/dashboard.html).
 */

const chartColorPalette = {
    primary: '#4f46e5',
    primaryLight: '#a5b4fc',
    success: '#22c55e',
    warning: '#f59e0b',
    danger: '#ef4444',
    neutral: '#94a3b8'
};

let completionChartInstance = null;
let taskStatusChartInstance = null;
let weeklyActivityChartInstance = null;

/**
 * Renders a doughnut chart of completion percentage per topic.
 * @param {string} canvasId
 * @param {Array<{topic: string, completion: number}>} progressData
 */
function renderCompletionChart(canvasId, progressData) {
    const chartCanvas = document.getElementById(canvasId);
    if (!chartCanvas || typeof Chart === 'undefined') return;

    const hasData = Array.isArray(progressData) && progressData.length > 0;
    const topicLabels = hasData ? progressData.map((entry) => entry.topic || 'Untitled') : ['No Progress'];
    const completionValues = hasData ? progressData.map((entry) => entry.completion || 0) : [0];

    if (completionChartInstance) {
        completionChartInstance.destroy();
    }

    completionChartInstance = new Chart(chartCanvas, {
        type: 'doughnut',
        data: {
            labels: topicLabels,
            datasets: [{
                data: completionValues,
                backgroundColor: [
                    chartColorPalette.primary,
                    chartColorPalette.success,
                    chartColorPalette.warning,
                    chartColorPalette.primaryLight,
                    chartColorPalette.neutral
                ],
                borderWidth: 0,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: 'Topic Completion' }
            }
        }
    });

    return completionChartInstance;
}

/**
 * Renders a bar chart showing task breakdown.
 * @param {string} canvasId
 * @param {Array<{status: string}>} taskData
 */
function renderTaskStatusChart(canvasId, taskData) {
    const chartCanvas = document.getElementById(canvasId);
    if (!chartCanvas || typeof Chart === 'undefined') return;

    const statusCounts = { completed: 0, pending: 0, overdue: 0 };

    if (Array.isArray(taskData)) {
        taskData.forEach((task) => {
            const taskStatus = (task.status || '').toLowerCase().trim();
            if (Object.prototype.hasOwnProperty.call(statusCounts, taskStatus)) {
                statusCounts[taskStatus] += 1;
            }
        });
    }

    if (taskStatusChartInstance) {
        taskStatusChartInstance.destroy();
    }

    taskStatusChartInstance = new Chart(chartCanvas, {
        type: 'bar',
        data: {
            labels: ['Completed', 'Pending', 'Overdue'],
            datasets: [{
                label: 'Tasks',
                data: [statusCounts.completed, statusCounts.pending, statusCounts.overdue],
                backgroundColor: [
                    chartColorPalette.success,
                    chartColorPalette.warning,
                    chartColorPalette.danger
                ],
                borderRadius: 6,
                maxBarThickness: 48
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Task Status Overview' }
            },
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } }
            }
        }
    });

    return taskStatusChartInstance;
}

/**
 * Renders a line chart of daily/weekly activity.
 * @param {string} canvasId
 * @param {Array<{label: string, value: number}>} weeklyActivityData
 */
function renderWeeklyActivityChart(canvasId, weeklyActivityData) {
    const chartCanvas = document.getElementById(canvasId);
    if (!chartCanvas || typeof Chart === 'undefined') return;

    const hasData = Array.isArray(weeklyActivityData) && weeklyActivityData.length > 0;
    const activityLabels = hasData ? weeklyActivityData.map((entry) => entry.label) : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const activityValues = hasData ? weeklyActivityData.map((entry) => entry.value) : [0, 0, 0, 0, 0, 0, 0];

    if (weeklyActivityChartInstance) {
        weeklyActivityChartInstance.destroy();
    }

    weeklyActivityChartInstance = new Chart(chartCanvas, {
        type: 'line',
        data: {
            labels: activityLabels,
            datasets: [{
                label: 'Learning Activity',
                data: activityValues,
                borderColor: chartColorPalette.primary,
                backgroundColor: 'rgba(79, 70, 229, 0.15)',
                fill: true,
                tension: 0.35,
                pointRadius: 4,
                pointBackgroundColor: chartColorPalette.primary
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Weekly Learning Consistency' }
            },
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } }
            }
        }
    });

    return weeklyActivityChartInstance;
}

/**
 * Global Initializer
 */
function initDashboardCharts(dashboardData = {}) {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded. Ensure Chart.js script tag precedes charts.js');
        return;
    }

    renderCompletionChart('completion-chart', dashboardData.progress || []);
    renderTaskStatusChart('task-status-chart', dashboardData.tasks || []);
    renderWeeklyActivityChart('weekly-activity-chart', dashboardData.weeklyActivity || []);
}