import json
import os

DATA_DIR = "data"


def save_data(users, projects, tasks, filename="tracker.json"):
# Builds the full file path (e.g., "data/tracker.json") in an OS-independent way
    filepath = os.path.join(DATA_DIR, filename)

    # Converts each object list into plain dicts via to_dict(), so it can be saved as JSON
    data = {
        "users": [u.to_dict() for u in users],
        "projects": [p.to_dict() for p in projects],
        "tasks": [t.to_dict() for t in tasks],
    }

    # Creates the data/ folder if it doesn't exist yet; no error if it already does
    os.makedirs(DATA_DIR, exist_ok=True)

    # Writes the data to disk as formatted (indented) JSON
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_data(filename="tracker.json"):
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(filepath):
        # First run — no data file yet, that's expected, not an error
        return [], [], []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        # File exists but is corrupted/unreadable — don't crash the whole app
        print(f"Warning: could not load {filepath} ({e}). Starting with empty data.")
        return [], [], []

    # Import model classes inside the function (rather than at the top)
    from models.user import User
    from models.project import Project
    from models.task import Task

    users = []
    users_by_id = {}        # dictionary mapping each user's id number to the actual User object
    for u in data.get("users", []):
        user = User(u["name"], u["email"])
        user.id = u["id"]  # overwrite the auto-assigned id with the original id from the file
        users.append(user)
        users_by_id[user.id] = user  # store in lookup dict so Projects/Tasks can find this User by id later

    projects = []
    projects_by_id = {}
    for p in data.get("projects", []):
        owner = users_by_id.get(p["owner_id"])
        project = Project(p["title"], p["description"], p["due_date"], owner=owner)  # creates a new Project linked to its owner
        project.id = p["id"]  # overwrite the auto-assigned id with the original id from the file
        if owner:
            owner.add_project(project)  # re-establish the User -> Project relationship
        projects.append(project)
        projects_by_id[project.id] = project  # store in lookup dict so Tasks can find this Project by id later

    tasks = []
    for t in data.get("tasks", []):
        project = projects_by_id.get(t["project_id"])
        assigned_to = users_by_id.get(t["assigned_to_id"])
        task = Task(t["title"], project=project, assigned_to=assigned_to, status=t["status"])  # creates a new Task linked to its project and assignee
        task.id = t["id"]  # overwrite the auto-assigned id with the original id from the file
        if project:
            project.add_task(task)  # re-establish the Project -> Task relationship
        tasks.append(task)

    # Re-link contributors now that all Users and Projects exist
    for p in data.get("projects", []):
        project = projects_by_id[p["id"]]
        for uid in p.get("contributor_ids", []):
            if uid in users_by_id:
                project.add_contributor(users_by_id[uid])

    return users, projects, tasks