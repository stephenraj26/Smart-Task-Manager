import sqlite3
from datetime import datetime

DB_PATH = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATETIME,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            remind_email INTEGER DEFAULT 1,
            remind_sms INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminder_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            channel TEXT,
            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)

    conn.commit()
    conn.close()

def create_user(username, email, phone, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, email, phone, password_hash)
        VALUES (?, ?, ?, ?)
    """, (username, email, phone, password_hash))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_task(user_id, title, description, due_date, priority, remind_email, remind_sms):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (user_id, title, description, due_date, priority, remind_email, remind_sms)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, due_date, priority, remind_email, remind_sms))
    conn.commit()
    conn.close()

def get_tasks_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC
    """, (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_task_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

def update_task(task_id, title, description, due_date, priority, remind_email, remind_sms):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks SET title=?, description=?, due_date=?, priority=?, remind_email=?, remind_sms=?
        WHERE id=?
    """, (title, description, due_date, priority, remind_email, remind_sms, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_pending_tasks_due_soon():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tasks.*, users.email, users.phone
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE tasks.status = 'pending'
        AND tasks.due_date BETWEEN datetime('now') AND datetime('now', '+24 hours')
        AND tasks.id NOT IN (
            SELECT task_id FROM reminder_logs
        )
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def log_reminder(task_id, channel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reminder_logs (task_id, channel)
        VALUES (?, ?)
    """, (task_id, channel))
    conn.commit()
    conn.close()
