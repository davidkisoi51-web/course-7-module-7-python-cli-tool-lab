# cli_tool.py

import argparse
import json
import os
from lib.models import Task, User

DB_FILE = "tasks_db.json"

def load_data():
    """Load users and tasks from a JSON file into memory."""
    if not os.path.exists(DB_FILE):
        return {}
    
    with open(DB_FILE, "r") as f:
        data = json.load(f)
        
    loaded_users = {}
    for user_name, task_list in data.items():
        user = User(user_name)
        for t_data in task_list:
            task = Task(t_data["title"])
            task.completed = t_data["completed"]
            user.tasks.append(task)
        loaded_users[user_name] = user
    return loaded_users

def save_data(users):
    """Save the current in-memory data back to the JSON file."""
    data = {}
    for user_name, user_obj in users.items():
        data[user_name] = [
            {"title": t.title, "completed": t.completed} for t in user_obj.tasks
        ]
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_task(args):
    users = load_data()
    user = users.get(args.user) or User(args.user)
    users[args.user] = user
    
    task = Task(args.title)
    user.add_task(task)
    save_data(users)  # Commit changes to disk

def complete_task(args):
    users = load_data()
    user = users.get(args.user)
    if user:
        for task in user.tasks:
            if task.title == args.title:
                task.complete()
                save_data(users)  # Commit changes to disk
                return
        print("❌ Task not found.")
    else:
        print("❌ User not found.")

# ... keep main() exactly the same as you wrote it ...