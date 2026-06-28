from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from auth import auth, login_required
from models import init_db, create_task, get_tasks_by_user, update_task_status, delete_task, get_task_by_id, update_task
from scheduler import start_scheduler
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.register_blueprint(auth)

with app.app_context():
    init_db()

start_scheduler()

@app.route("/")
@login_required
def dashboard():
    user_id = session["user_id"]
    username = session["username"]
    tasks = get_tasks_by_user(user_id)
    return render_template("dashboard.html", tasks=tasks, username=username)

@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        user_id = session["user_id"]
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]
        remind_email = 1 if "remind_email" in request.form else 0
        remind_sms = 1 if "remind_sms" in request.form else 0

        create_task(user_id, title, description, due_date, priority, remind_email, remind_sms)

        flash("Task added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("task_form.html", task=None)

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = get_task_by_id(task_id)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]
        remind_email = 1 if "remind_email" in request.form else 0
        remind_sms = 1 if "remind_sms" in request.form else 0

        update_task(task_id, title, description, due_date, priority, remind_email, remind_sms)

        flash("Task updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("task_form.html", task=task)

@app.route("/update_task/<int:task_id>/<status>")
@login_required
def update_task_route(task_id, status):
    update_task_status(task_id, status)
    flash("Task status updated!", "success")
    return redirect(url_for("dashboard"))

@app.route("/delete_task/<int:task_id>")
@login_required
def delete_task_route(task_id):
    delete_task(task_id)
    flash("Task deleted!", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
