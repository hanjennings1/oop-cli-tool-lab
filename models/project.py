class Project:
    """Represents a project owned by a user, containing tasks."""

    _id_counter = 1

    def __init__(self, title, description="", due_date=None, owner=None):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner          # the User who owns this project
        self.tasks = []             # one-to-many: Project -> Tasks
        self.contributors = []      # many-to-many: Project <-> Users

    def add_task(self, task):
        self.tasks.append(task)

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)

    @property
    def is_complete(self):
        """A project is complete when it has tasks and all are done."""
        return bool(self.tasks) and all(task.status == "complete" for task in self.tasks)

    def __str__(self):
        return f"Project(id={self.id}, title={self.title}, tasks={len(self.tasks)}, due={self.due_date})"

    def __repr__(self):
        return f"Project(id={self.id!r}, title={self.title!r}, owner={self.owner.name if self.owner else None!r})"