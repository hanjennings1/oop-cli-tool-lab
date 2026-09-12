# Project Management CLI Tool
**Completed Sept 12, 2026** 

## Overview
A command-line tool for managing users, projects, and tasks, built for the
Summative Lab (Python Project Management CLI Tool). Data is persisted locally
as JSON, and CLI output is styled using the `rich` package.

## Features

- Create and list users
- Add projects to a user and list a user's projects
- Add tasks to a project
- Mark tasks as complete
- Data persists between runs via a local JSON file (`data/tracker.json`)
- Styled table output for list commands (via `rich`)

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/hanjennings1/oop-cli-tool-lab.git
   cd oop-cli-tool-lab
```

2. Install dependencies with `pipenv`:
```bash
   pipenv install
```

3. Activate the virtual environment:
```bash
   pipenv shell
```

## Usage

All commands are run via `python main.py <command> [options]`.

### Add a user
```bash
python main.py add-user --name "Alex" --email "alex@example.com"
```

### List all users
```bash
python main.py list-users
```

### Add a project to a user
```bash
python main.py add-project --user "Alex" --title "CLI Tool" --description "School project" --due-date "2026-12-01"
```

### List a user's projects
```bash
python main.py list-projects --user "Alex"
```

### Add a task to a project
```bash
python main.py add-task --project "CLI Tool" --title "Write file I/O logic"
```

### Mark a task complete
```bash
python main.py complete-task --task 1
```

## Project Structure
```
oop-cli-tool-lab/
├── main.py # CLI entry point (argparse commands)
├── models/
│ ├── user.py # Person, User classes
│ ├── project.py # Project class
│ └── task.py # Task class
├── utils/
│ └── file_io.py # JSON save/load logic
├── tests/
│ ├── test_models.py # Unit tests for User/Project/Task and file I/O
│ └── test_cli.py # CLI-level tests using main(argv)
├── data/
│ └── tracker.json # Generated at runtime; not committed
├── Pipfile # Dependency tracking (pipenv)
└── README.md
```

## Running Tests

```bash
python -m pytest tests/
```

## Known Issues / Limitations

- User, project, and task lookups (`--user`, `--project`) match by **name/title**,
  not by ID. If two users share a name, or two projects share a title, the
  first match found will be used.
- `Project.contributors` (many-to-many between projects and users) is modeled
  and persisted, but there is currently no CLI command to add a contributor.
- There is no `edit`/`delete` command for users, projects, or tasks.
- `Task.assigned_to` supports a single user, not multiple contributors per task.

## Development Notes

This project was built incrementally: models and relationships first, then
file persistence, then the CLI commands were wired to real logic, then styled
output (`rich`) was added, and finally a test suite (`pytest`) was written to
cover the model logic, file I/O round-tripping, and CLI commands. 
Git history reflects this via feature branches and pull requests for each stage.
