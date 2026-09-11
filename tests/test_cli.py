import os
import shutil
import pytest
from main import main
import utils.file_io as file_io


@pytest.fixture
def temp_data_dir(monkeypatch, tmp_path):
    # Redirect file_io's DATA_DIR to a temporary folder for this test only,
    # so we never touch the real data/tracker.json
    test_dir = tmp_path / "data"
    monkeypatch.setattr(file_io, "DATA_DIR", str(test_dir))
    yield test_dir
    # tmp_path is automatically cleaned up by pytest after the test


def test_add_user_cli(temp_data_dir, capsys):
    main(["add-user", "--name", "Test User", "--email", "test@example.com"])
    captured = capsys.readouterr()
    assert "Created user: User" in captured.out
    assert "Test User" in captured.out


def test_list_users_empty_cli(temp_data_dir, capsys):
    main(["list-users"])
    captured = capsys.readouterr()
    assert "No users found" in captured.out