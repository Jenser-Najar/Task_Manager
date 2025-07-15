
// ========== Dark Mode Toggle ========== //
const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;

function setDarkMode(enabled) {
    if (enabled) {
        body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'true');
    } else {
        body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'false');
    }
}

function toggleDarkMode() {
    setDarkMode(!body.classList.contains('dark-mode'));
}

if (darkModeToggle) {
    darkModeToggle.addEventListener('click', toggleDarkMode);
    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        setDarkMode(true);
    }
}

// ========== Toast Notification ========== //
function showToast(message, duration = 2000) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.style.display = 'block';
    toast.style.opacity = 1;
    setTimeout(() => {
        toast.style.opacity = 0;
        setTimeout(() => { toast.style.display = 'none'; }, 300);
    }, duration);
}

// ========== Task Actions (Event Delegation) ========== //
document.addEventListener('DOMContentLoaded', () => {
    // Ocultar 'No tasks yet.' si se agrega una tarea por AJAX
    // AJAX Add Task
    const addTaskForm = document.querySelector('form');
    const taskList = document.querySelector('ul');
    if (addTaskForm && taskList) {
        addTaskForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(addTaskForm);
            fetch(addTaskForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'ok' && data.task_html) {
                        // Remove 'No tasks yet.' if present
                        const emptyMsg = taskList.querySelector('li');
                        if (emptyMsg && emptyMsg.textContent.trim() === 'No tasks yet.') {
                            emptyMsg.remove();
                        }
                        // Insert new task at the top
                        const temp = document.createElement('div');
                        temp.innerHTML = data.task_html;
                        const newTask = temp.firstElementChild;
                        if (newTask) {
                            taskList.insertBefore(newTask, taskList.firstChild);
                        }
                        addTaskForm.reset();
                        showToast('Task added!');
                    } else if (data.status === 'error' && data.errors) {
                        showToast(data.errors, 3000);
                    } else {
                        showToast('Error adding task.');
                    }
                })
                .catch(() => showToast('Error adding task.'));
        });
    }

    // Complete/Toggle Task & Delete Task (Event Delegation)
    document.body.addEventListener('click', function (e) {
        if (e.target.classList.contains('complete-btn')) {
            e.preventDefault();
            const taskId = e.target.getAttribute('data-task-id');
            fetch(`/toggle/${taskId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCSRFToken() },
            })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'ok') {
                        showToast('Task status updated!');
                        setTimeout(() => window.location.reload(), 600);
                    } else {
                        showToast('Error updating task.');
                    }
                });
        }
        // Delete Task
        if (e.target.classList.contains('delete-btn')) {
            e.preventDefault();
            const taskId = e.target.getAttribute('data-task-id');
            fetch(`/delete/${taskId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCSRFToken() },
            })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'ok') {
                        showToast('Task deleted!');
                        setTimeout(() => window.location.reload(), 600);
                    } else {
                        showToast('Error deleting task.');
                    }
                });
        }
    });
});

// ========== CSRF Token Helper ========== //
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    // Fallback: try to find in hidden input
    const input = document.querySelector('input[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
}
