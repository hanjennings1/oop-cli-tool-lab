import argparse
from utils.file_io import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task


def main():
    parser = argparse.ArgumentParser(
        prog="project-tracker",
        description="A CLI tool for managing users, projects, and tasks."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add-user
    add_user_parser = subparsers.add_parser("add-user", help="Create a new user")
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=True)

    # list-users
    subparsers.add_parser("list-users", help="List all users")

    # add-project
    add_project_parser = subparsers.add_parser("add-project", help="Add a project to a user")
    add_project_parser.add_argument("--user", required=True, help="User name or ID")
    add_project_parser.add_argument("--title", required=True)
    add_project_parser.add_argument("--description", default="")
    add_project_parser.add_argument("--due-date", default=None)

    # list-projects
    list_projects_parser = subparsers.add_parser("list-projects", help="List projects for a user")
    list_projects_parser.add_argument("--user", required=True)

    # add-task
    add_task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)

    # complete-task
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_task_parser.add_argument("--task", required=True, help="Task ID")

    args = parser.parse_args()

    users, projects, tasks = load_data()

    if args.command == "add-user":
    # Create a new User from the --name/--email flags
        user = User(args.name, args.email)
        users.append(user)
        save_data(users, projects, tasks)  # persist the new user immediately
        print(f"Created user: {user}")

    elif args.command == "list-users":
        # Read-only command [no save_data() call needed]
        if not users:
            print("No users found.")
        else:
            for user in users:
                print(user)  # uses User.__str__ for friendly CLI output

    elif args.command == "add-project":
        # Look up the User whose name matches --user; None if no match found
        owner = next((u for u in users if u.name == args.user), None)
        if owner is None:
            print(f"No user found with name '{args.user}'.")
        else:
            project = Project(args.title, args.description, args.due_date, owner=owner)
            owner.add_project(project)  # re-establish the User -> Project relationship
            projects.append(project)
            save_data(users, projects, tasks)  # persist the new project immediately
            print(f"Created project: {project}")

    elif args.command == "list-projects":
        # Look up the User whose name matches --user; None if no match found
        owner = next((u for u in users if u.name == args.user), None)
        if owner is None:
            print(f"No user found with name '{args.user}'.")
        else:
            # Use the User -> Project relationship directly, rather than
            # filtering the full projects list
            if not owner.projects:
                print(f"{owner.name} has no projects.")
            else:
                for project in owner.projects:
                    print(project)  # uses Project.__str__ for friendly CLI output

    elif args.command == "add-task":
        # Look up the Project whose title matches --project; None if no match found
        project = next((p for p in projects if p.title == args.project), None)
        if project is None:
            print(f"No project found with title '{args.project}'.")
        else:
            task = Task(args.title, project=project)
            project.add_task(task)  # re-establish the Project -> Task relationship
            tasks.append(task)
            save_data(users, projects, tasks)  # persist the new task immediately
            print(f"Created task: {task}")

    elif args.command == "complete-task":
        # Look up the Task whose id matches --task; None if no match found
        task = next((t for t in tasks if str(t.id) == args.task), None)
        if task is None:
            print(f"No task found with id '{args.task}'.")
        else:
            task.mark_complete()  # uses the Task.status setter, which validates the value
            save_data(users, projects, tasks)  # persist the status change
            print(f"Marked complete: {task}")

if __name__ == "__main__":
    main()