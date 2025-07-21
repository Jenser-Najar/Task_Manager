# Task Manager

A modern, full stack Django web application for managing tasks with AJAX, dark mode, responsive design, and a robust backend. Instantly add, complete, and delete tasks with a beautiful and user-friendly interface.

## Features

- Add, complete, and delete tasks instantly (AJAX, no page reloads)
- Responsive and modern UI with dark mode support
- Toast notifications for user feedback
- Clean, scalable Django backend
- Secure with CSRF protection
- Professional code structure and documentation

## Technologies Used

- Python 3 & Django
- HTML5, CSS3, Tailwind CSS
- JavaScript (ES6+)
- AJAX (fetch API)
- SQLite (default, easy to switch to PostgreSQL/MySQL)
- Docker-ready (optional)

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- (Optional) Docker

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jenser-Najar/Task_Manager.git
   cd Task_Manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Open [http://localhost:8000](http://localhost:8000) in your browser.

### Docker (optional)

```bash
docker build -t taskmanager .
docker run -p 8000:8000 taskmanager
```

## Project Structure

- `tasks/` – Main app: models, views, forms, templates, static files
- `taskmanager/` – Project settings and URLs
- `templates/` – HTML templates (with partials for AJAX)
- `static/` – CSS and JavaScript (dark mode, AJAX, toast notifications)

## Main Views

- **Task List:** List all tasks, add new tasks (AJAX or regular POST)
- **Complete Task:** Toggle completion status
- **Delete Task:** Remove tasks (AJAX or fallback GET)
- **Toggle Completion (AJAX):** Update task status instantly

## Screenshots

_Add screenshots here if you have them!_

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
