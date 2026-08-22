# Django Multi-User To-Do Application

A clean Django app with user authentication and personal task management, styled with Tailwind CSS.

## Setup & Run

```bash
cd "/Users/mrcom/Desktop/DJango/Project 2"

# Run migrations
python3 manage.py makemigrations todos
python3 manage.py migrate

# (Optional) Create a superuser for admin
python3 manage.py createsuperuser

# Start the development server
python3 manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

## Routes

| URL | Description |
|-----|-------------|
| `/signup/` | Create a new account |
| `/login/` | Log in |
| `/logout/` | Log out (POST) |
| `/` | Task dashboard (login required) |
| `/task/<id>/edit/` | Edit a task |
| `/task/<id>/toggle/` | Mark complete / undo |
| `/task/<id>/delete/` | Delete a task |
| `/admin/` | Django admin |

## Features

- Sign up with username, email, and password
- Login & logout
- Each user sees only their own tasks
- Add, edit, complete, and delete tasks
- Tailwind CSS styling via CDN
- CSRF protection on all forms
