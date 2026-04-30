================================================================
  TEAM TASK MANAGER — Full-Stack Django Application
================================================================

A web app for teams to create projects, assign tasks, and track
progress with role-based access control (Admin / Member).

----------------------------------------------------------------
TECH STACK
----------------------------------------------------------------
  Backend   : Python 3.11 + Django 5.0
  Database  : SQLite (dev) / PostgreSQL (production via Railway)
  Frontend  : HTML5 + CSS3 (Django Templates)
  Auth      : Django built-in authentication
  Deploy    : Railway (gunicorn + whitenoise)

----------------------------------------------------------------
KEY FEATURES
----------------------------------------------------------------
  - User signup / login / logout
  - Create projects and invite team members
  - Role-based access (Admin vs Member)
      * Admin: create/edit/delete tasks, manage team
      * Member: view tasks, update status of own tasks
  - Task creation, assignment, status tracking
      (To Do / In Progress / Done)
  - Priority levels (Low / Medium / High) and due dates
  - Dashboard: task counts, upcoming work, overdue items
  - REST API endpoints (JSON) for tasks
  - Validations and proper relational data model

----------------------------------------------------------------
PROJECT STRUCTURE
----------------------------------------------------------------
  taskmanager/        Django project settings & root URLs
  accounts/           Signup / login (uses built-in auth)
  projects/           Project + Membership models, views
  tasks/              Task model, dashboard, REST API
  templates/          HTML templates
  static/css/         Stylesheet
  manage.py           Django CLI entry point
  requirements.txt    Python dependencies
  Procfile            Railway/Heroku process definition
  railway.json        Railway deployment config
  runtime.txt         Python version for Railway

----------------------------------------------------------------
LOCAL SETUP (Windows / macOS / Linux)
----------------------------------------------------------------
  1. Clone the repo:
        git clone <your-repo-url>
        cd team_task_manager

  2. Create a virtual environment:
        python -m venv venv
        # Windows:  venv\Scripts\activate
        # macOS/Linux:  source venv/bin/activate

  3. Install dependencies:
        pip install -r requirements.txt

  4. Run migrations (creates SQLite db.sqlite3):
        python manage.py migrate

  5. Create a superuser (for /admin access):
        python manage.py createsuperuser

  6. Start the dev server:
        python manage.py runserver

  7. Open: http://127.0.0.1:8000/

----------------------------------------------------------------
USAGE FLOW
----------------------------------------------------------------
  1. Sign up at /accounts/signup/
  2. Create a project at /projects/new/
     (creator becomes Admin automatically)
  3. On the project page, add team members by username
     and choose their role (Admin or Member).
  4. Admins create tasks and assign them to members.
  5. Members log in and update task status from the
     dashboard or task edit page.
  6. Dashboard shows totals, overdue tasks, and projects.

----------------------------------------------------------------
REST API ENDPOINTS
----------------------------------------------------------------
  GET   /api/projects/<id>/tasks/      List tasks in a project
  POST  /api/tasks/<id>/status/        Update a task's status
        Body: {"status": "todo|in_progress|done"}

  All endpoints require an authenticated session.

----------------------------------------------------------------
DEPLOYMENT — RAILWAY
----------------------------------------------------------------
  1. Push code to GitHub.
  2. On https://railway.app -> New Project ->
     "Deploy from GitHub repo" -> select your repo.
  3. Add a PostgreSQL plugin (Railway auto-injects
     DATABASE_URL).
  4. Set environment variables in Railway:
        SECRET_KEY            = <a long random string>
        DEBUG                 = False
        ALLOWED_HOSTS         = .railway.app,.up.railway.app
        CSRF_TRUSTED_ORIGINS  = https://*.railway.app,https://*.up.railway.app
  5. Deploy. The release command runs migrations
     automatically (see Procfile / railway.json).
  6. Open the generated public URL.

  Create a superuser in production via Railway shell:
        python manage.py createsuperuser

----------------------------------------------------------------
DATA MODEL
----------------------------------------------------------------
  User (Django built-in)
    └─ Membership (role: admin | member) ──┐
                                           ▼
                                        Project
                                           │
                                           ▼
                                        Task (status, priority,
                                              due_date, assignee)

----------------------------------------------------------------
SECURITY NOTES
----------------------------------------------------------------
  - CSRF protection enabled on all forms.
  - Permission checks in every view (membership + role).
  - Passwords hashed with Django's PBKDF2.
  - Static files served via WhiteNoise (compressed + hashed).
  - Always change SECRET_KEY and set DEBUG=False in production.

----------------------------------------------------------------
SUBMISSION CHECKLIST
----------------------------------------------------------------
  [x] Live URL          (Railway deployment)
  [x] GitHub repo       (push this folder)
  [x] README.txt        (this file)
  [ ] 2-5 min demo video (record signup -> project ->
                          add member -> create task ->
                          update status -> dashboard)

================================================================
