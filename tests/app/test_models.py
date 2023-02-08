from sqlmodel import Session, select

from app.db_function import create_user_test
from app.models import LogApi, User


def test_check_valid_password():
    user: User = User()
    user.generate_password("cat")
    assert user.verify_password("cat") is True


def test_check_invalid_password():
    user: User = User()
    user.generate_password("cat")
    assert user.verify_password("dog") is False


class RequestClassMock:
    def __init__(self, method: str, request_json: dict, url: str = ""):
        self.method = method
        self.json = request_json
        self.url = url

    def get_json(self):
        return self.json


def test_save_log_api(app):
    # Create user test
    with app.app_context():
        user: User = create_user_test()

    is_saved: bool = LogApi.save_log(
        _request=RequestClassMock(
            method="POST", request_json={"document": "00000000000", "cashback": "20.10"}
        ),
        response_json={},
        user=user,
        status_code=201,
    )

    query = select(LogApi).where(LogApi.user_id == user.id)
    with Session(app.engine) as session:
        log_api: LogApi = session.execute(query).scalars().one()

    assert is_saved is True
    assert log_api.status_code == 201
    assert log_api.response == {}
    assert log_api.request == {"document": "00000000000", "cashback": "20.10"}
    assert log_api.method == "POST"
    assert log_api.url == ""
