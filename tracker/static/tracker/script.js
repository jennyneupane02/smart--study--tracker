// Return a cookie value by name. This is used to send the CSRF token with fetch requests.
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

// Toggle the mobile navigation menu when the hamburger button is clicked.
const menuToggle = document.querySelector('#menu-toggle');
const navLinks = document.querySelector('#nav-links');
if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
    });
}

// When a user clicks a complete button, update the task with fetch without reloading the page.
document.querySelectorAll('.complete-btn').forEach(button => {
    button.addEventListener('click', () => {
        const taskId = button.dataset.taskId;
        fetch(`/api/tasks/${taskId}/toggle/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const taskItem = document.querySelector(`#task-${data.task_id}`);
                if (taskItem) {
                    taskItem.classList.toggle('done', data.completed);
                }
                button.textContent = data.completed ? 'Undo' : 'Complete';

                const completedCount = document.querySelector('#completed-count');
                const totalCount = document.querySelector('#total-count');
                const progressFill = document.querySelector('#progress-fill');
                const progressLabel = document.querySelector('#progress-label');

                if (completedCount) completedCount.textContent = data.completed_count;
                if (totalCount) totalCount.textContent = data.total_count;
                if (progressFill) progressFill.style.width = `${data.percent}%`;
                if (progressLabel) progressLabel.textContent = `${data.percent}% complete`;
            }
        })
        .catch(error => console.log('Error updating task:', error));
    });
});
