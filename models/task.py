VALID_STATUSES = {"pending", "in progress", "complete"}


class Task:
    """Represents a task belonging to a project."""

    _id_counter = 1

    def __init__(self, title, project=None, assigned_to=None, status="pending"):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.project = project          # back-reference to owning Project
        self.assigned_to = assigned_to  # a User, or None
        self.status = status            # uses the @property/setter below

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}. Must be one of {VALID_STATUSES}")
        self._status = value

    def mark_complete(self):
        self.status = "complete"

    def __str__(self):
        # Human-readable output for CLI display; avoid crashing on unassigned tasks
        assignee = self.assigned_to.name if self.assigned_to else "Unassigned"
        return f"Task(id={self.id}, title={self.title}, status={self.status}, assigned_to={assignee})"

    def __repr__(self):
    # Debug-friendly output:
        # !r wraps string values in quotes so it's clear this is raw/debug data
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status!r})"