from apscheduler.schedulers.background import BackgroundScheduler
from models import get_pending_tasks_due_soon, log_reminder
from notifications import send_email, send_sms
import atexit

def send_reminders():
    print("Scheduler running — checking for due tasks...")

    tasks = get_pending_tasks_due_soon()

    for task in tasks:
        task_id = task["id"]
        task_title = task["title"]
        due_date = task["due_date"]
        email = task["email"]
        phone = task["phone"]
        remind_email = task["remind_email"]
        remind_sms = task["remind_sms"]

        if remind_email:
            success = send_email(email, task_title, due_date)
            if success:
                log_reminder(task_id, "email")

        if remind_sms and phone:
            success = send_sms(phone, task_title, due_date)
            if success:
                log_reminder(task_id, "sms")

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=send_reminders,
        trigger="interval",
        hours=1,
        id="reminder_job"
    )

    scheduler.start()
    print("Scheduler started — reminders will run every hour.")

    atexit.register(lambda: scheduler.shutdown())

    return scheduler
