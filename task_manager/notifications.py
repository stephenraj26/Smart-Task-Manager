import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_ADDRESS = os.environ.get("MAIL_ADDRESS")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")

def send_email(to_email, task_title, due_date):
    try:
        msg = MIMEMultipart()
        msg["From"] = MAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = f"Reminder: '{task_title}' is due soon!"

        body = f"""
Hi there!

This is a reminder that your task:

  Task  : {task_title}
  Due   : {due_date}

is due within the next 24 hours.

Login to Smart Task Manager to update your progress.

- Smart Task Manager
        """

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(MAIL_ADDRESS, MAIL_PASSWORD)
        server.sendmail(MAIL_ADDRESS, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email} for task: {task_title}")
        return True

    except Exception as e:
        print(f"Email failed: {e}")
        return False

def send_sms(to_phone, task_title, due_date):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)

        message = client.messages.create(
            body=f"Reminder: Your task '{task_title}' is due on {due_date}. Login to Smart Task Manager to update your progress.",
            from_=TWILIO_PHONE,
            to=to_phone
        )

        print(f"SMS sent to {to_phone}, SID: {message.sid}")
        return True

    except Exception as e:
        print(f"SMS failed: {e}")
        return False
