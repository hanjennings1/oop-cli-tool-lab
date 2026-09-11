from models.user import User
from models.task import Task
from models.project import Project
import os
from utils.file_io import save_data, load_data


''' USER TESTS '''
def test_user_creation():
# Verify a valid User is created with the expected attributes
    user = User("Alex", "alex@example.com")
    assert user.name == "Alex"
    assert user.email == "alex@example.com"
    assert user.projects == []  # new users should start with an empty project list

def test_user_invalid_email_raises_error():
# Verify the @email.setter validation actually rejects a bad email
    try:
        User("Alex", "not-an-email")
        assert False, "Expected ValueError for invalid email"  # fails the test if no error was raised
    except ValueError:
        pass  # this is the expected outcome — validation worked correctly


''' TASK TESTS '''
def test_task_creation_defaults_to_pending():
# A new Task with no status specified should default to "pending"
    task = Task("Write tests")
    assert task.title == "Write tests"
    assert task.status == "pending"
    assert task.project is None
    assert task.assigned_to is None

def test_task_invalid_status_raises_error():
# Verify the @status.setter rejects any value not in VALID_STATUSES
    try:
        Task("Write tests", status="not-a-real-status")
        assert False, "Expected ValueError for invalid status"
    except ValueError:
        pass  # expected outcome — validation worked correctly

def test_mark_complete_sets_status():
# Verify mark_complete() actually changes status to "complete"
    task = Task("Write tests")
    task.mark_complete()
    assert task.status == "complete"


''' PROJECT TESTS '''
def test_project_is_complete_false_with_no_tasks():
# A project with zero tasks is not "complete" — nothing to be complete
    project = Project("CLI Tool")
    assert project.is_complete is False

def test_project_is_complete_false_with_incomplete_task():
# A project with at least one non-complete task should not be complete
    project = Project("CLI Tool")
    task = Task("Write tests", project=project)
    project.add_task(task)
    assert project.is_complete is False

def test_project_is_complete_true_when_all_tasks_done():
# A project is complete only when every task's status is "complete"
    project = Project("CLI Tool")
    task = Task("Write tests", project=project)
    project.add_task(task)
    task.mark_complete()
    assert project.is_complete is True



''' THROW-AWAY TEST'''
def test_save_and_load_round_trip():
    # Use a separate test file so we don't touch the real data/tracker.json
    test_filename = "test_tracker.json"

    user = User("Alex", "alex@example.com")
    project = Project("CLI Tool", owner=user)
    user.add_project(project)
    task = Task("Write tests", project=project, assigned_to=user)
    project.add_task(task)

    save_data([user], [project], [task], filename=test_filename)

    loaded_users, loaded_projects, loaded_tasks = load_data(filename=test_filename)

    # Confirm the data round-tripped correctly, including relationships
    assert len(loaded_users) == 1
    assert loaded_users[0].name == "Alex"
    assert len(loaded_projects) == 1
    assert loaded_projects[0].title == "CLI Tool"
    assert loaded_projects[0].owner.name == "Alex"  # relationship preserved
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Write tests"
    assert loaded_tasks[0].project.title == "CLI Tool"  # relationship preserved

    # Clean up the test file so repeated test runs stay isolated
    test_filepath = os.path.join("data", test_filename)
    if os.path.exists(test_filepath):
        os.remove(test_filepath)