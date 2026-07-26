/**
 * script.js
 * -----------------------------------------------------------------------
 * Shared utilities loaded on every page (via the base template, before
 * charts.js / dashboard.js / quiz.js / roadmap.js). Provides:
 *   - fetchJson()       generic JSON fetch wrapper
 *   - getEmbeddedData() reads server-rendered JSON out of a page
 *   - showToast()       lightweight notification helper
 * Also wires up the login and register forms.
 *
 * IDS USED (from the shared id list): email, password, login-btn, register-btn
 *
 * ID ADDED OUT OF NECESSITY: full-name
 *   The shared id list has no id covering the Users.full_name column, so the
 *   register form needs one extra field. #full-name was added to
 *   templates/register.html to fill that gap; every other id below already
 *   existed in the shared list.
 */

const apiBaseUrl = '';

/**
 * Wrapper around fetch() that sends/expects JSON and normalizes errors.
 * @param {string} url
 * @param {RequestInit & {body?: any}} options
 */
async function fetchJson(url, options = {}) {
    const requestOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            ...(options.headers || {})
        },
        ...options
    };

    if (requestOptions.body && typeof requestOptions.body !== 'string') {
        requestOptions.body = JSON.stringify(requestOptions.body);
    }

    const response = await fetch(`${apiBaseUrl}${url}`, requestOptions);
    const contentType = response.headers.get('content-type') || '';
    const responseData = contentType.includes('application/json') ? await response.json() : null;

    if (!response.ok) {
        const errorMessage = (responseData && responseData.message) || `Request failed with status ${response.status}`;
        throw new Error(errorMessage);
    }

    return responseData;
}

/**
 * Reads server-rendered JSON embedded by Jinja, e.g.:
 *   <script type="application/json" id="dashboard-data">{{ dashboard_data | tojson }}</script>
 * Returns null if the tag is missing/invalid so callers can fall back to fetchJson().
 * @param {string} elementId
 */
function getEmbeddedData(elementId) {
    const dataElement = document.getElementById(elementId);
    if (!dataElement) {
        return null;
    }

    try {
        return JSON.parse(dataElement.textContent);
    } catch (error) {
        console.error(`Failed to parse embedded data for #${elementId}:`, error);
        return null;
    }
}

/**
 * Shows a small dismissible toast message. Expects a #toast-container element
 * on the page (add <div id="toast-container"></div> once in base.html).
 * Falls back to console output if that container is missing.
 * @param {string} message
 * @param {'info'|'error'} toastType
 */
function showToast(message, toastType = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        console[toastType === 'error' ? 'error' : 'log'](message);
        return;
    }

    const toastElement = document.createElement('div');
    toastElement.className = `toast toast-${toastType}`;
    toastElement.textContent = message;
    toastContainer.appendChild(toastElement);

    setTimeout(() => toastElement.remove(), 4000);
}

/**
 * Wires up the login form (#email, #password, #login-btn) if present on the page.
 */
function initLoginForm() {
    const loginButton = document.getElementById('login-btn');
    if (!loginButton) {
        return;
    }

    loginButton.addEventListener('click', async (event) => {
        event.preventDefault();

        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const emailValue = emailInput ? emailInput.value.trim() : '';
        const passwordValue = passwordInput ? passwordInput.value : '';

        if (!emailValue || !passwordValue) {
            showToast('Please enter your email and password.', 'error');
            return;
        }

        loginButton.disabled = true;

        try {
            await fetchJson('/login', {
                method: 'POST',
                body: { email: emailValue, password: passwordValue }
            });
            window.location.href = '/dashboard';
        } catch (error) {
            showToast(error.message || 'Login failed. Please try again.', 'error');
        } finally {
            loginButton.disabled = false;
        }
    });
}

/**
 * Wires up the register form (#full-name, #email, #password, #register-btn) if present.
 */
function initRegisterForm() {
    const registerButton = document.getElementById('register-btn');
    if (!registerButton) {
        return;
    }

    registerButton.addEventListener('click', async (event) => {
        event.preventDefault();

        const fullNameInput = document.getElementById('full-name');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');

        const fullNameValue = fullNameInput ? fullNameInput.value.trim() : '';
        const emailValue = emailInput ? emailInput.value.trim() : '';
        const passwordValue = passwordInput ? passwordInput.value : '';

        if (!fullNameValue || !emailValue || !passwordValue) {
            showToast('Please fill in all fields.', 'error');
            return;
        }

        registerButton.disabled = true;

        try {
            await fetchJson('/register', {
                method: 'POST',
                body: { full_name: fullNameValue, email: emailValue, password: passwordValue }
            });
            window.location.href = '/login';
        } catch (error) {
            showToast(error.message || 'Registration failed. Please try again.', 'error');
        } finally {
            registerButton.disabled = false;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initLoginForm();
    initRegisterForm();
});