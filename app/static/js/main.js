/**
 * Main JavaScript for Online Job Portal
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Setup AJAX Bookmarking
    setupBookmarkButtons();

    // Setup Demo Account Autofill
    setupDemoCredentials();
});

/**
 * Handle bookmark toggle via fetch API
 */
function setupBookmarkButtons() {
    const bookmarkBtns = document.querySelectorAll('.btn-bookmark-ajax');
    bookmarkBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();

            const jobId = btn.dataset.jobId;
            if (!jobId) return;

            try {
                const response = await fetch(`/seeker/save-toggle/${jobId}`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json'
                    }
                });

                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }

                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        const icon = btn.querySelector('i');
                        if (data.is_saved) {
                            btn.classList.add('bookmarked');
                            if (icon) {
                                icon.classList.remove('bi-bookmark');
                                icon.classList.add('bi-bookmark-fill');
                            }
                        } else {
                            btn.classList.remove('bookmarked');
                            if (icon) {
                                icon.classList.remove('bi-bookmark-fill');
                                icon.classList.add('bi-bookmark');
                            }
                        }
                        showToast(data.message || 'Bookmark updated!');
                    }
                } else if (response.status === 401 || response.status === 403) {
                    window.location.href = '/auth/login';
                }
            } catch (err) {
                console.error('Error toggling bookmark:', err);
            }
        });
    });
}

/**
 * Quick Fill Demo Credentials on Login Page
 */
function setupDemoCredentials() {
    const fillSeekerBtn = document.getElementById('fillSeekerDemo');
    const fillEmployerBtn = document.getElementById('fillEmployerDemo');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    if (fillSeekerBtn && emailInput && passwordInput) {
        fillSeekerBtn.addEventListener('click', () => {
            emailInput.value = 'candidate@example.com';
            passwordInput.value = 'password123';
            highlightInputs(emailInput, passwordInput);
        });
    }

    if (fillEmployerBtn && emailInput && passwordInput) {
        fillEmployerBtn.addEventListener('click', () => {
            emailInput.value = 'recruiter@techcorp.com';
            passwordInput.value = 'password123';
            highlightInputs(emailInput, passwordInput);
        });
    }
}

function highlightInputs(...inputs) {
    inputs.forEach(input => {
        input.classList.add('is-valid');
        setTimeout(() => input.classList.remove('is-valid'), 1500);
    });
}

/**
 * Modern floating toast message
 */
function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container-dynamic');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container-dynamic';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1099';
        document.body.appendChild(container);
    }

    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-white bg-dark border-0 shadow-lg';
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body d-flex align-items-center gap-2">
                <i class="bi bi-check-circle-fill text-success fs-5"></i>
                <span>${message}</span>
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
    toast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}
