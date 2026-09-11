import argparse


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

    # Dispatch — real logic comes once models exist
    print(f"Command received: {args.command} (not yet implemented)")


if __name__ == "__main__":
    main()