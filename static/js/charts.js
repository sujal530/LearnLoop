/**
 * charts.js
 * -----------------------------------------------------------------------
 * Renders the analytics charts shown inside #dashboard-container.
 * Uses Chart.js (loaded via CDN <script> tag in templates/dashboard.html).
 *
 * SCOPE OF THIS FILE
 * This file only renders charts from data it is given. It does not fetch
 * data itself, so it does not need to know which route or table the data
 * came from. dashboard.js (owned by another dev) is responsible for
 * loading data from the backend and calling initDashboardCharts() below.
 *
 * EXPECTED CANVAS IDS (add these inside #dashboard-container in
 * templates/dashboard.html — no existing id in the naming list covers
 * charts, so these three are new and kept consistent/kebab-case):
 *   - completion-chart      (topic completion, from Progress table)
 *   - task-status-chart     (task status breakdown, from Tasks table)
 *   - weekly-activity-chart (learning velocity / daily consistency)
 *
 * EXPECTED DATA SHAPES (field names match the existing DB columns):
 *   progressData        -> [{ topic, completion }, ...]
 *   taskData             -> [{ title, status, deadline }, ...]
 *   weeklyActivityData   -> [{ label, value }, ...]  e.g. [{label:"Mon",value:3}]
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
 * @param {string} canvasId - id of the <canvas> element
 * @param {Array<{topic: string, completion: number}>} progressData
 */
function renderCompletionChart(canvasId, progressData) {
    const chartCanvas = document.getElementById(canvasId);
    if (!chartCanvas || typeof Chart === 'undefined') {
        return;
    }

    const hasData = Array.isArray(progressData) && progressData.length > 0;
    const topicLabels = hasData ? progressData.map((entry) => entry.topic) : ['No progress yet'];
    const completionValues = hasData ? progressData.map((entry) => entry.completion) : [100];

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
 * Renders a bar chart showing how many tasks are completed, pending, or overdue.
 * @param {string} canvasId - id of the <canvas> element
 * @param {Array<{status: string}>} taskData
 */
function renderTaskStatusChart(canvasId, taskData) {
    const chartCanvas = document.getElementById(canvasId);
    if (!chartCanvas || typeof Chart === 'undefined') {
        return;
    }

    const statusCounts = { completed: 0, pending: 0, overdue: 0 };

    if (Array.isArray(taskData)) {
        taskData.forEach((task) => {
            const taskStatus = (task.status || '').toLowerCase();
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
 * Renders a line chart of learning velocity / daily consistency.
 * @param {string} canvasId - id of the <canvas> element
 * @param {Array<{label: string, value: number}>} weeklyActivityData
 */
function renderWeeklyActivityChart(canvasId, weeklyActivityData) {
    const chartCanvas = document.getElementById(canvasId);
    if (!chartCanvas || typeof Chart === 'undefined') {
        return;
    }

    const hasData = Array.isArray(weeklyActivityData) && weeklyActivityData.length > 0;
    const activityLabels = hasData ? weeklyActivityData.map((entry) => entry.label) : [];
    const activityValues = hasData ? weeklyActivityData.map((entry) => entry.value) : [];

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
 * Convenience entry point: renders every dashboard chart whose canvas is
 * present on the page. Call this from dashboard.js once data has been
 * fetched, e.g.:
 *
 *   initDashboardCharts({
 *       progress: progressData,
 *       tasks: taskData,
 *       weeklyActivity: weeklyActivityData
 *   });
 *
 * @param {{progress?: Array, tasks?: Array, weeklyActivity?: Array}} dashboardData
 */
function initDashboardCharts(dashboardData = {}) {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded. Add the Chart.js <script> tag before charts.js.');
        return;
    }

    renderCompletionChart('completion-chart', dashboardData.progress || []);
    renderTaskStatusChart('task-status-chart', dashboardData.tasks || []);
    renderWeeklyActivityChart('weekly-activity-chart', dashboardData.weeklyActivity || []);
}