class Project:
    """Represents a project owned by a user, containing tasks."""

    _id_counter = 1     # class attribute: auto-incrementing ID shared by all Projects

    def __init__(self, title, description="", due_date=None, owner=None):
        # Assign and increment the unique ID for this Project
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner          # the User who owns this project
        self.tasks = []             # one-to-many: Project -> Tasks
        self.contributors = []      # many-to-many: Project <-> Users

    def add_task(self, task):
    # Attaches a Task to this Project's task list
        self.tasks.append(task)

    def add_contributor(self, user):
    # Adds a User as a contributor, avoiding duplicate entries
        if user not in self.contributors:
            self.contributors.append(user)

    @property
    def is_complete(self):
        """A project is complete when it has tasks and all are done."""
        # Calculated each time it's accessed (rather than stored)
        return bool(self.tasks) and all(task.status == "complete" for task in self.tasks)

    def __str__(self):
    # Human-readable output for CLI display
        return f"Project(id={self.id}, title={self.title}, tasks={len(self.tasks)}, due={self.due_date})"

    def __repr__(self):
    # Debug-friendly output; shows owner's name (or None) rather than the full User object
        return f"Project(id={self.id!r}, title={self.title!r}, owner={self.owner.name if self.owner else None!r})"

    def to_dict(self):
    # Converts this Project into a plain dict so it can be saved as JSON
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_id": self.owner.id if self.owner else None,
            "task_ids": [t.id for t in self.tasks],
            "contributor_ids": [u.id for u in self.contributors],
        }