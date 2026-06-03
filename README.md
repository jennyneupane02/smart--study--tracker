# Smart Study Tracker

[![Django CI](../../actions/workflows/django.yml/badge.svg)](../../actions/workflows/django.yml)

Smart Study Tracker is a Django web application designed for students who want to organize assignments, study sessions, subjects, and daily study goals in one place. The application allows users to register, log in, create subjects, add study tasks, record study sessions, set daily goals, and track progress from a dashboard. The project uses Django on the back end, SQLite for the database, Django templates for the interface, and JavaScript with fetch to update task completion without a full page reload.

## Distinctiveness and Complexity

This project is distinct from the standard projects in the course because it is not a social network, e-commerce website, email application, or simple feed-based project. The main purpose is personal academic planning and study progress tracking. Users are not following each other, posting public content, buying products, or checking out. Instead, each user has a private productivity workspace where they manage their own subjects, tasks, study sessions, and goals. This makes the application different in purpose and structure from the earlier assignments.

The project is also more complex than a basic CRUD app because it combines several related features into one connected system. A user can create subjects, connect tasks and study sessions to those subjects, set daily study goals, and view progress on a dashboard. The models are related through ForeignKey relationships, and all information is filtered by the logged-in user. This means the application must handle authentication carefully so that each user only sees and changes their own data.

Another complex part is the JavaScript interaction. On the tasks page, users can mark a task complete or undo completion without reloading the page. The JavaScript code listens for a button click, sends a POST request with fetch to a Django API endpoint, receives a JsonResponse, and then updates the DOM by changing the task style, button text, completed count, and progress bar. This is more advanced than a normal form submission because the front end and back end communicate asynchronously.

The project also includes responsive design. The dashboard and task pages use CSS Grid and media queries so that the layout works on both desktop and mobile screens. On a wide screen, cards appear in two columns. On a small phone screen, the cards stack into one column, and the navigation menu becomes collapsible. This makes the project more realistic and usable than a desktop-only web page.

## Files Created

### `manage.py`
This is the standard Django command-line utility. It is used to run the server, create migrations, apply migrations, and run tests.

### `requirements.txt`
This file lists the Python package required to run the project. The project uses Django.

### `.gitignore`
This file prevents unnecessary files such as `db.sqlite3`, Python cache files, and virtual environment folders from being committed to GitHub.

### `.github/workflows/django.yml`
This optional GitHub Actions workflow runs Django tests automatically when code is pushed to GitHub.

### `smartstudy/settings.py`
This file contains the Django project settings, including installed apps, database settings, static file settings, templates, and authentication redirects.

### `smartstudy/urls.py`
This file connects the main Django project to the `tracker` app URLs and the Django Admin route.

### `smartstudy/wsgi.py` and `smartstudy/asgi.py`
These files are standard Django deployment entry points. They allow the project to run with WSGI or ASGI servers.

### `tracker/models.py`
This file defines the database models for the project. It includes `Subject`, `Task`, `StudySession`, and `DailyGoal`. These models represent the real information users store in the app.

### `tracker/forms.py`
This file defines Django forms used for registration, subjects, tasks, study sessions, and daily goals. The task and study session forms filter subjects so users only see their own subjects.

### `tracker/views.py`
This file contains the main application logic. It includes views for the home page, registration, dashboard, tasks, subjects, study sessions, goals, editing tasks, deleting tasks, and the API endpoint for toggling task completion.

### `tracker/urls.py`
This file defines all application routes, including the dashboard, tasks, subjects, sessions, goals, login, logout, registration, and JSON API endpoint.

### `tracker/admin.py`
This file registers all project models in Django Admin so they can be managed from the admin panel.

### `tracker/tests.py`
This file contains simple tests for authentication protection and the task completion API.

### `tracker/templates/tracker/layout.html`
This is the base layout template. All other templates extend this file. It includes the navigation bar, message display, static CSS link, static JavaScript link, and `{% block content %}`.

### `tracker/templates/tracker/index.html`
This template displays the public home page and changes the call-to-action depending on whether the user is logged in.

### `tracker/templates/tracker/register.html`
This template displays the registration form for new users.

### `tracker/templates/tracker/login.html`
This template displays the login form for existing users.

### `tracker/templates/tracker/dashboard.html`
This template displays task progress, today's study time, goal progress, and upcoming pending tasks.

### `tracker/templates/tracker/tasks.html`
This template displays the task creation form and the user's task list. It includes buttons that JavaScript uses to complete or undo tasks without reloading the page.

### `tracker/templates/tracker/edit_task.html`
This template allows users to edit an existing task.

### `tracker/templates/tracker/delete_task.html`
This template asks users to confirm before deleting a task.

### `tracker/templates/tracker/subjects.html`
This template allows users to create subjects and view their saved subjects.

### `tracker/templates/tracker/sessions.html`
This template allows users to record study sessions and view recent sessions.

### `tracker/templates/tracker/goals.html`
This template allows users to set daily goals and view recent goals.

### `tracker/static/tracker/styles.css`
This file contains all custom CSS. It includes layout styling, cards, forms, buttons, progress bars, task styling, and mobile responsiveness using media queries.

### `tracker/static/tracker/script.js`
This file contains all JavaScript. It controls the mobile navigation menu and uses fetch to toggle task completion without reloading the page.

## How to Run the Application

1. Clone the repository or download the project folder.

2. Open a terminal and move into the project folder:

```bash
cd capstone
```

3. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On Mac or Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create database migrations:

```bash
python manage.py makemigrations
```

6. Apply migrations:

```bash
python manage.py migrate
```

7. Create an admin user if you want to use Django Admin:

```bash
python manage.py createsuperuser
```

8. Start the development server:

```bash
python manage.py runserver
```

9. Open the application in your browser:

```text
http://127.0.0.1:8000/
```

10. Register a new account, create subjects, add tasks, record study sessions, set goals, and test the dashboard.

<<<<<<< HEAD
## Lesson 14 Enhancements

For Lesson 14, I completed two enhancements: **Option D – Testing** and **Option E – CI/CD Pipeline**. I chose these because they make the project stronger and more reliable. Instead of only adding visual features, these enhancements help prove that the application works correctly and that future code changes will not silently break important behavior.

### Option D – Testing

I expanded the Django test suite in `tracker/tests.py`. The project now includes 10 meaningful tests across three test classes:

- `TaskModelTests` checks model behavior, including the task title string and the `is_overdue` property.
- `DashboardViewTests` checks that the dashboard requires login, loads correctly for an authenticated user, and calculates progress data.
- `TaskAPITests` checks the JavaScript JSON endpoint that toggles task completion, including the returned JSON shape, login protection, and protection against editing another user's task.

To see this enhancement working:

1. Open a terminal in the project folder.
2. Run:

```bash
python manage.py test
```

3. The terminal should show that all tests pass. In my local test run, Django reported:

```text
Ran 10 tests

OK
```

### Option E – CI/CD Pipeline

I added a GitHub Actions workflow in `.github/workflows/django.yml`. This workflow runs automatically every time code is pushed to GitHub. It installs the project dependencies, runs migrations, and then runs the Django test suite with:

```bash
python manage.py test
```

Automated testing matters because it helps catch problems early. If a future change breaks authentication, model behavior, or the JSON endpoint, the GitHub Actions workflow will fail and show that something needs to be fixed before submission or deployment.

To see this enhancement working:

1. Push the project to GitHub.
2. Open the repository on GitHub.
3. Click the **Actions** tab.
4. Open the latest **Django CI** workflow run.
5. Confirm that the workflow has a green check mark and passed successfully.

### Files Created or Modified for Lesson 14

- `tracker/tests.py` — expanded from a small test file into a full test suite with 10 tests.
- `.github/workflows/django.yml` — updated to install dependencies, run migrations, and run the test suite automatically.
- `tracker/migrations/0001_initial.py` — added the initial database migration for the tracker app models.
- `README.md` — added this Lesson 14 Enhancements section and a GitHub Actions status badge.

### New Dependencies

No new dependencies were added. The project still uses the existing packages listed in `requirements.txt`.

### Screenshots to Include in the PDF Submission

- Screenshot 1: Terminal showing `python manage.py test` with all 10 tests passing.
- Screenshot 2: GitHub Actions page showing the **Django CI** workflow passing.

=======
>>>>>>> c8c388d8bdfc879a21b310b6891e71f79993ce43
## Additional Information

The application uses Django authentication, so users must register and log in before they can access the dashboard, tasks, subjects, sessions, or goals. The app filters all main data by the current user, which prevents one user from viewing another user's tasks or study records.

The JavaScript code is written in a separate file, not inline in the HTML. It includes DOM manipulation and a fetch request to a Django view that returns a JsonResponse. The main interactive feature is the Complete button on each task. When clicked, it updates the database and changes the page immediately without a full reload.

The templates use `{% block %}`, `{% for %}`, `{% if %}`, and `{% url %}`. URLs are not hardcoded in the templates. The project is also mobile responsive because the CSS uses media queries and a responsive grid layout.

Before submitting, run these commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

For CS50W submission, push the project to a public GitHub repository on the required branch:

```bash
git checkout -b web50/projects/2020/x/capstone
git add .
git commit -m "Complete capstone project"
git push origin web50/projects/2020/x/capstone
```

Make sure this README.md file is at the root of the repository, not inside a subfolder. Also record a video of five minutes or less showing the application working live. The video should begin with a slide or text showing the edX username and GitHub username, then demonstrate the app features without walking through the code.
