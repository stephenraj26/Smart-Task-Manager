import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import models
from models import init_db, create_user, get_user_by_username, create_task, get_tasks_by_user, update_task_status, delete_task

TEST_DB = "test_tasks.db"

def setup_function():
    models.DB_PATH = TEST_DB
    init_db()

def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_create_and_get_user():
    models.DB_PATH = TEST_DB
    create_user("testuser", "test@gmail.com", "+91999999999", "hashed_password")
    user = get_user_by_username("testuser")
    assert user is not None
    assert user["email"] == "test@gmail.com"

def test_create_and_get_task():
    models.DB_PATH = TEST_DB
    create_user("taskuser", "task@gmail.com", "+91888888888", "hashed_password")
    user = get_user_by_username("taskuser")
    create_task(user["id"], "Test Task", "Description", "2026-12-31 10:00", "high", 1, 0)
    tasks = get_tasks_by_user(user["id"])
    assert len(tasks) > 0
    assert tasks[0]["title"] == "Test Task"

def test_update_task_status():
    models.DB_PATH = TEST_DB
    create_user("statususer", "status@gmail.com", "+91777777777", "hashed_password")
    user = get_user_by_username("statususer")
    create_task(user["id"], "Status Task", "", "2026-12-31 10:00", "medium", 1, 0)
    tasks = get_tasks_by_user(user["id"])
    update_task_status(tasks[0]["id"], "done")
    updated = get_tasks_by_user(user["id"])
    assert updated[0]["status"] == "done"

def test_delete_task():
    models.DB_PATH = TEST_DB
    create_user("deleteuser", "delete@gmail.com", "+91666666666", "hashed_password")
    user = get_user_by_username("deleteuser")
    create_task(user["id"], "Delete Task", "", "2026-12-31 10:00", "low", 0, 0)
    tasks = get_tasks_by_user(user["id"])
    delete_task(tasks[0]["id"])
    remaining = get_tasks_by_user(user["id"])
    assert len(remaining) == 0
