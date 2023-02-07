from app.models import User


def test_check_valid_password():
    user: User = User()
    user.generate_password("cat")
    assert user.verify_password("cat") is True


def test_check_invalid_password():
    user: User = User()
    user.generate_password("cat")
    assert user.verify_password("dog") is False
