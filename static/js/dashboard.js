/**
 * dashboard.js
 * -----------------------------------------------------------------------
 * Main dashboard script for Sujal's learning app.
 */

// Safety fallbacks if script.js loads out of order
if (typeof getEmbeddedData !== 'function') {
    window.getEmbeddedData = function(id) {
        const scriptTag = document.getElementById(id);
        if (scriptTag && scriptTag.textContent) {
            try { return JSON.parse(scriptTag.textContent); } catch (e) { return null; }
        }
        return null;
    };
}

if (typeof fetchJson !== 'function') {
    window.fetchJson = async function(url, options = {}) {
        const requestOptions = {
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', ...(options.headers || {}) },
            ...options
        };
        if (requestOptions.body && typeof requestOptions.body !== 'string') {
            requestOptions.body = JSON.stringify(requestOptions.body);
        }
        const response = await fetch(url, requestOptions);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    };
}

if (typeof showToast !== 'function') {
    window.showToast = function(msg, type = 'info') {
        console.log(`[Toast ${type}]: ${msg}`);
    };
}

/**
 * Loads dashboard data or provides clean fallbacks
 */
async function loadDashboardData() {
    const embeddedData = getEmbeddedData('dashboard-data');
    if (embeddedData) {
        return embeddedData;
    }

    try {
        const [progressData, taskData] = await Promise.all([
            fetchJson('/progress').catch(() => []),
            fetchJson('/tasks').catch(() => [])
        ]);
        return { progress: progressData || [], tasks: taskData || [] };
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        return { progress: [], tasks: [] };
    }
}

/**
 * Computes overall completion percentage
 */
function calculateOverallCompletion(progressData) {
    if (!Array.isArray(progressData) || progressData.length === 0) return 0;
    const totalCompletion = progressData.reduce((sum, entry) => sum + (entry.completion || 0), 0);
    const result = Math.round(totalCompletion / progressData.length);
    return isNaN(result) ? 0 : result;
}

/**
 * Renders upcoming tasks list and task counter
 */
function renderUpcomingTasksList(taskData) {
    const upcomingTasksList = document.getElementById('upcoming-tasks-list');
    const taskCountBadge = document.getElementById('upcoming-tasks-count');

    const upcomingTasks = (taskData || [])
        .filter((task) => task.status !== 'completed')
        .sort((a, b) => {
            const timeA = a.deadline ? new Date(a.deadline).getTime() : Infinity;
            const timeB = b.deadline ? new Date(b.deadline).getTime() : Infinity;
            return timeA - timeB;
        });

    if (taskCountBadge) {
        taskCountBadge.textContent = String(upcomingTasks.length);
    }

    if (!upcomingTasksList) return;

    if (upcomingTasks.length > 0) {
        const tasksHTML = upcomingTasks.map(task => {
            const formattedDate = task.deadline 
                ? new Date(task.deadline).toLocaleDateString() 
                : (task.due_label || 'No deadline');
                
            return `
                <li class="upcoming-task-item" id="task-item-${task.id || ''}">
                    <span class="task-icon">${task.icon || '📌'}</span>
                    <div class="task-meta">
                        <p class="task-title">${task.title}</p>
                        <p class="task-type">${task.type || 'General Task'}</p>
                    </div>
                    <span class="task-due">${formattedDate}</span>
                </li>
            `;
        }).join('');

        upcomingTasksList.innerHTML = tasksHTML;
    } else {
        upcomingTasksList.innerHTML = '<li class="upcoming-task-item" style="justify-content:center; opacity:0.6;">No upcoming tasks!</li>';
    }
}

/**
 * Injects and manages the New Task Modal
 */
function ensureTaskModalExists() {
    let modal = document.getElementById('dynamic-task-modal');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.id = 'dynamic-task-modal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: 10000;
        align-items: center;
        justify-content: center;
    `;

    modal.innerHTML = `
        <div style="background: var(--bg-card, #fff); color: var(--text-color, #333); padding: 2rem; border-radius: 12px; width: 90%; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); position: relative;">
            <h3 style="margin-top:0; margin-bottom: 1rem;">Create New Task</h3>
            <form id="dynamic-task-form">
                <div style="margin-bottom: 1rem;">
                    <label style="display:block; margin-bottom: 0.5rem; font-size: 0.9rem;">Task Title</label>
                    <input type="text" id="dynamic-task-title" required placeholder="e.g. Read Chapter 4" style="width: 100%; padding: 0.6rem; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box;" />
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <label style="display:block; margin-bottom: 0.5rem; font-size: 0.9rem;">Due Date</label>
                    <input type="date" id="dynamic-task-date" style="width: 100%; padding: 0.6rem; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box;" />
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                    <button type="button" id="close-dynamic-modal-btn" class="btn btn-outline" style="padding: 0.5rem 1rem;">Cancel</button>
                    <button type="submit" class="btn btn-primary" style="padding: 0.5rem 1rem;">Save Task</button>
                </div>
            </form>
        </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('close-dynamic-modal-btn')?.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    const form = document.getElementById('dynamic-task-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const titleInput = document.getElementById('dynamic-task-title');
            const dateInput = document.getElementById('dynamic-task-date');

            const newTask = {
                title: titleInput ? titleInput.value.trim() : '',
                deadline: dateInput ? dateInput.value : '',
                status: 'pending'
            };

            try {
                await fetchJson('/tasks', {
                    method: 'POST',
                    body: newTask
                });

                showToast('Task added successfully!', 'success');
                form.reset();
                modal.style.display = 'none';

                const data = await loadDashboardData();
                renderUpcomingTasksList(data.tasks);
            } catch (err) {
                console.error('Error saving task:', err);
                showToast('Could not save task.', 'error');
            }
        });
    }

    return modal;
}

function initNewTaskButton() {
    const newTaskBtn = document.getElementById('new-task-btn');
    if (!newTaskBtn) return;

    newTaskBtn.addEventListener('click', () => {
        const modal = ensureTaskModalExists();
        modal.style.display = 'flex';
    });
}

/**
 * Injects and manages the Ask Mentor Modal
 */
function ensureMentorModalExists() {
    let modal = document.getElementById('dynamic-mentor-modal');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.id = 'dynamic-mentor-modal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: 10000;
        align-items: center;
        justify-content: center;
    `;

    modal.innerHTML = `
        <div style="background: var(--bg-card, #fff); color: var(--text-color, #333); padding: 2rem; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin:0; font-size: 1.25rem;">✦ Ask Your Mentor</h3>
                <button type="button" id="close-mentor-modal-x" style="background:none; border:none; font-size:1.2rem; cursor:pointer;">✕</button>
            </div>
            <form id="dynamic-mentor-form">
                <div style="margin-bottom: 1rem;">
                    <label style="display:block; margin-bottom: 0.5rem; font-size: 0.9rem;">What would you like advice or help with?</label>
                    <textarea id="mentor-question-input" rows="4" required placeholder="e.g., How should I prepare for my upcoming quiz?" style="width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-family: inherit; resize: vertical;"></textarea>
                </div>
                <div id="mentor-response-area" style="display: none; margin-bottom: 1rem; padding: 0.75rem; background: #f0f4f8; border-radius: 6px; font-size: 0.9rem;"></div>
                <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                    <button type="button" id="close-mentor-modal-btn" class="btn btn-outline" style="padding: 0.5rem 1rem;">Close</button>
                    <button type="submit" id="send-mentor-btn" class="btn btn-primary" style="padding: 0.5rem 1rem;">Send Question</button>
                </div>
            </form>
        </div>
    `;

    document.body.appendChild(modal);

    const closeModal = () => { modal.style.display = 'none'; };
    document.getElementById('close-mentor-modal-x')?.addEventListener('click', closeModal);
    document.getElementById('close-mentor-modal-btn')?.addEventListener('click', closeModal);

    const form = document.getElementById('dynamic-mentor-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = document.getElementById('mentor-question-input');
            const responseArea = document.getElementById('mentor-response-area');
            const submitBtn = document.getElementById('send-mentor-btn');

            const question = input ? input.value.trim() : '';
            if (!question) return;

            try {
                if (submitBtn) submitBtn.disabled = true;
                if (responseArea) {
                    responseArea.style.display = 'block';
                    responseArea.textContent = 'Thinking...';
                }

                const data = await fetchJson('/mentor', {
                    method: 'POST',
                    body: { question: question }
                }).catch(() => null);

                if (responseArea) {
                    responseArea.textContent = (data && data.reply) 
                        ? data.reply 
                        : "Question sent! Your mentor will review it shortly.";
                }

                showToast('Question sent to mentor!', 'success');
                if (input) input.value = '';
            } catch (err) {
                console.error('Error asking mentor:', err);
                showToast('Could not reach mentor right now.', 'error');
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }

    return modal;
}

function initAskMentorButton() {
    const askMentorBtn = document.getElementById('ask-mentor-btn');
    if (!askMentorBtn) return;

    askMentorBtn.addEventListener('click', () => {
        const modal = ensureMentorModalExists();
        modal.style.display = 'flex';
    });
}

/**
 * Quick Notes functionality
 */
function initQuickNotes() {
    const saveNoteBtn = document.getElementById('save-note-btn');
    const noteInput = document.getElementById('quick-notes-input');
    const noteStatus = document.getElementById('notes-status');

    if (!saveNoteBtn || !noteInput) return;

    saveNoteBtn.addEventListener('click', async () => {
        const noteText = noteInput.value.trim();
        if (!noteText) {
            showToast('Note cannot be empty.', 'error');
            return;
        }

        try {
            if (noteStatus) noteStatus.textContent = 'Saving...';
            await fetchJson('/notes', {
                method: 'POST',
                body: { content: noteText }
            }).catch(() => {});
            showToast('Note saved!', 'success');
            if (noteStatus) noteStatus.textContent = 'Saved';
        } catch (err) {
            console.error('Error saving note:', err);
            showToast('Could not save note.', 'error');
        }
    });
}

/**
 * Page Initialization
 */
async function initDashboardPage() {
    const data = await loadDashboardData();

    const completionEl = document.getElementById('overall-completion-value');
    if (completionEl && data.progress && data.progress.length > 0) {
        completionEl.textContent = `${calculateOverallCompletion(data.progress)}%`;
    }

    renderUpcomingTasksList(data.tasks);

    initNewTaskButton();
    initAskMentorButton();
    initQuickNotes();
}

document.addEventListener('DOMContentLoaded', initDashboardPage);