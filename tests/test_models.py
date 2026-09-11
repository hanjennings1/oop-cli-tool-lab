from models.user import User


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