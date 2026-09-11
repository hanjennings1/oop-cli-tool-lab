class Person:
    """Base class representing a person with a name and email."""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"{self.name} <{self.email}>"


class User(Person):
    """Represents a system user who owns projects."""

    _id_counter = 1  # class attribute: auto-incrementing ID

    def __init__(self, name, email):
        super().__init__(name, email)
        self.id = User._id_counter
        User._id_counter += 1
        self.projects = []  # one-to-many: User -> Projects

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError(f"Invalid email: {value}")
        self._email = value

    def add_project(self, project):
        self.projects.append(project)

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, projects={len(self.projects)})"

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"