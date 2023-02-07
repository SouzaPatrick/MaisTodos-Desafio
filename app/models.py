import json
from datetime import datetime
from typing import Optional

from flask import current_app
from sqlmodel import JSON, Column, Field, Relationship, Session, SQLModel, String
from werkzeug.security import check_password_hash, generate_password_hash


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", String, unique=True))
    password_hash: str

    log_api: list["LogApi"] = Relationship(back_populates="user")

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cashback_percentage: int


class LogApi(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    method: str
    request: dict = Field(default={}, sa_column=Column(JSON))
    response: dict = Field(default={}, sa_column=Column(JSON))
    status_code: int
    url: str

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="log_api")

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def save_log(_request, user: User, response_json: dict, status_code: int) -> bool:

        try:
            log_api = LogApi(
                method=_request.method,
                user_id=user.id,
                request=_request.get_json(),
                response=response_json,
                status_code=status_code,
                url=_request.url,
            )
        except AttributeError:
            log_api = LogApi(
                method=_request.method,
                user_id=user.id,
                request=json.loads(_request.body.decode("utf-8").replace("'", '"')),
                response=response_json,
                status_code=status_code,
                url=_request.url,
            )
        except Exception:
            return False

        with Session(current_app.engine) as session:
            session.add(log_api)
            session.commit()

        return True
