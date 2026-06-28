# Smart Task Manager

A full-stack web application built with Flask and SQLite that helps users manage tasks with automated email and SMS reminders.

## Features

- User registration and login with secure password hashing
- Create, edit, delete, and update task status
- Set task priority (low, medium, high)
- Automated email reminders via Gmail SMTP
- Automated SMS reminders via Twilio
- Background scheduler checks for due tasks every hour
- Reminder logs to prevent duplicate notifications

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Authentication | Werkzeug (password hashing), Flask sessions |
| Email | Python smtplib (Gmail SMTP) |
| SMS | Twilio API |
| Scheduler | APScheduler |
| Frontend | HTML, Jinja2, Bootstrap 5 |

## Project Structure

```
task_manager/
├── app.py               # Flask app, routes
├── auth.py              # Register, login, logout, login_required
├── models.py            # Database schema and queries
├── notifications.py     # Email and SMS sending logic
├── scheduler.py         # APScheduler background jobs
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── task_form.html
├── static/
│   └── style.css
├── tests/
│   └── test_models.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/stephenraj26/smart-task-manager.git
cd smart-task-manager
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```
SECRET_KEY=your_secret_key_here
MAIL_ADDRESS=your_gmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH=your_twilio_auth_token
TWILIO_PHONE=+1234567890
```

> **Gmail Setup:** Enable 2-factor authentication on your Gmail account, then go to Google Account → Security → App Passwords → generate a password for "Mail".

> **Twilio Setup:** Sign up at twilio.com, get your Account SID, Auth Token, and a free phone number.

### 5. Run the application

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`

### 6. Run tests

```bash
python -m pytest tests/
```

## How It Works

1. User registers an account with email and optional phone number
2. User creates tasks with title, description, due date, priority, and reminder preferences
3. APScheduler runs every hour in the background
4. If a task is due within 24 hours and hasn't been reminded yet, the scheduler triggers email and/or SMS reminders
5. Each reminder is logged in the `reminder_logs` table to prevent duplicates

## Database Schema

```
users          → id, username, email, phone, password_hash, created_at
tasks          → id, user_id, title, description, due_date, priority, status, remind_email, remind_sms, created_at
reminder_logs  → id, task_id, channel, sent_at
```

## Author

**Stephen Raj G**
- GitHub: [@stephenraj26](https://github.com/stephenraj26)
- LinkedIn: [stephen-raj-g](https://linkedin.com/in/stephen-raj-g)
