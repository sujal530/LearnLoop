/**
 * script.js
 * -----------------------------------------------------------------------
 * Shared utilities loaded on every page.
 * Provides helper functions for toast notifications and embedded data.
 */

const apiBaseUrl = '';

/**
 * Wrapper around fetch() that sends/expects JSON and normalizes errors.
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
 * Reads server-rendered JSON embedded by Jinja.
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
 * Shows a small dismissible toast message.
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
 * Validates registration form passwords client-side without blocking submission.
 */
function initRegisterValidation() {
    const registerForm = document.getElementById('register-form');
    if (!registerForm) return;

    registerForm.addEventListener('submit', (event) => {
        const password = document.getElementById('password')?.value;
        const confirmPassword = document.getElementById('confirm_password')?.value;

        if (password && confirmPassword && password !== confirmPassword) {
            event.preventDefault(); // Stop form submission ONLY if passwords don't match
            showToast('Passwords do not match.', 'error');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initRegisterValidation();
});