// --- CSRF helper ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
// Modo oscuro
let darkModeSetting = localStorage.getItem('darkMode');
if (darkModeSetting === 'enabled') {
    document.body.classList.add('dark-mode');
}

function toggleDarkMode() {
    document.body.classList.add('fade-transition');
    document.body.classList.remove('fade-in');

    setTimeout(() => {
        document.body.classList.toggle('dark-mode');

        localStorage.setItem(
            'darkMode',
            document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled'
        );

        document.body.classList.add('fade-in');

        setTimeout(() => {
            document.body.classList.remove('fade-transition');
            document.body.classList.remove('fade-in');
        }, 500);
    }, 100);
}

// --- codigo b: AJAX para completar tarea ---
function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.style.display = 'block';
    toast.style.opacity = '1';
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => { toast.style.display = 'none'; }, 400);
    }, 1800);
}

function toggleTaskCompletion(event, taskId) {
    event.preventDefault();
    fetch(`/toggle/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                const btn = event.target;
                const li = btn.closest('li');
                if (data.completed) {
                    li.classList.add('completed');
                    btn.innerHTML = '🔄 Marcar como pendiente';
                    showToast('¡Tarea marcada como completada!');
                } else {
                    li.classList.remove('completed');
                    btn.innerHTML = '✅ Marcar como completada';
                    showToast('¡Tarea marcada como pendiente!');
                }
            }
        })
        .catch(error => {
            showToast('Ocurrió un error');
            console.error('Error:', error);
        });
}
// --- fin codigo b ---

// --- AJAX para eliminar tarea ---
function deleteTaskAjax(event, taskId) {
    event.preventDefault();
    if (!confirm('¿Estás seguro que quieres eliminar esta tarea?')) return;
    fetch(`/delete/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                const btn = event.target;
                const li = btn.closest('li');
                li.remove();
                showToast('¡Tarea eliminada!');
            }
        })
        .catch(error => {
            showToast('Ocurrió un error');
            console.error('Error:', error);
        });
}
// --- fin AJAX eliminar tarea ---

// --- AJAX para agregar nueva tarea ---
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form[method="post"]');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'ok' && data.task) {
                        // Crear el nuevo elemento de tarea
                        const ul = document.querySelector('ul');
                        const li = document.createElement('li');
                        if (data.task.completed) {
                            li.classList.add('completed');
                        }
                        li.innerHTML = `
                            <strong>${data.task.title}</strong> - ${data.task.description}
                            ${data.task.completed ? '✅' : '❌'}
                            <div style="margin-top: 10px;">
                                <button class="action-btn complete-btn" data-task-id="${data.task.id}" onclick="toggleTaskCompletion(event, ${data.task.id})">
                                    ${data.task.completed ? '🔄 Marcar como pendiente' : '✅ Marcar como completada'}
                                </button>
                                <button class="action-btn delete-btn" data-task-id="${data.task.id}" onclick="deleteTaskAjax(event, ${data.task.id})">🗑️ Eliminar</button>
                            </div>
                        `;
                        if (ul) {
                            // Si la lista solo tiene el mensaje de vacío, lo quitamos
                            if (ul.children.length === 1 && ul.children[0].textContent.includes('No hay tareas')) {
                                ul.innerHTML = '';
                            }
                            ul.prepend(li);
                        }
                        form.reset();
                        showToast('¡Tarea agregada!');
                    } else if (data.errors) {
                        showToast('Error: ' + JSON.stringify(data.errors));
                    } else {
                        showToast('Ocurrió un error');
                    }
                })
                .catch(error => {
                    showToast('Ocurrió un error');
                    console.error('Error:', error);
                });
        });
    }
});
// --- fin AJAX agregar tarea ---
