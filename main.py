import argparse
from utils.file_io import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task

from rich.console import Console
from rich.table import Table


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
    console = Console()


    if args.command == "add-user":
    # Create a new User from the --name/--email flags
        user = User(args.name, args.email)
        users.append(user)
        save_data(users, projects, tasks)  # persist the new user immediately
        print(f"Created user: {user}")

    elif args.command == "list-users":      # USING RICH TO FORMAT
        # Read-only command [no save_data() call needed]
        if not users:
            console.print("[yellow]No users found.[/yellow]")  # styled warning text, no table needed
        else:
            table = Table(title="Users")  # rich table with a heading, replaces plain print loop
            table.add_column("ID", style="cyan")        # column-level color styling
            table.add_column("Name", style="magenta")
            table.add_column("Email")                    # no style = default color
            table.add_column("Projects", justify="right")  # right-align since it's a number

            for user in users:
                # add_row() requires string values, so ints get converted with str()
                table.add_row(str(user.id), user.name, user.email, str(len(user.projects)))

            console.print(table)  # renders the table with borders/colors; regular print() won't work here

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

    elif args.command == "list-projects":      # USING RICH TO FORMAT
        # Look up the User whose name matches --user; None if no match found
        owner = next((u for u in users if u.name == args.user), None)
        if owner is None:
            console.print(f"[yellow]No user found with name '{args.user}'.[/yellow]")
        else:
            # Use the User -> Project relationship directly, rather than
            # filtering the full projects list
            if not owner.projects:
                console.print(f"[yellow]{owner.name} has no projects.[/yellow]")
            else:
                table = Table(title=f"Projects for {owner.name}")
                table.add_column("ID", style="cyan")
                table.add_column("Title", style="magenta")
                table.add_column("Due Date")
                table.add_column("Tasks", justify="right")

                for project in owner.projects:
                    table.add_row(
                        str(project.id),
                        project.title,
                        str(project.due_date) if project.due_date else "—",
                        str(len(project.tasks)),
                    )

                console.print(table)

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