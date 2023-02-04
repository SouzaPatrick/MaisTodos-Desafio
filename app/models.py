import json
from datetime import datetime
from typing import Optional

from sqlmodel import JSON, Column, Field, Session, SQLModel

from app.database import engine


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cashback_percentage: int


class LogApi(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    app: str
    method: str
    request: dict = Field(default={}, sa_column=Column(JSON))
    response: dict = Field(default={}, sa_column=Column(JSON))
    status_code: int

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def save_log(_request, response_json: dict, app: str, status_code: int) -> bool:

        try:
            log_api = LogApi(
                app=app,
                method=_request.method,
                request=_request.get_json(),
                response=response_json,
                status_code=status_code,
            )
        except AttributeError:
            log_api = LogApi(
                app=app,
                method=_request.method,
                request=json.loads(_request.body.decode("utf-8").replace("'", '"')),
                response=response_json,
                status_code=status_code,
            )
        except Exception:
            return False

        with Session(engine) as session:
            session.add(log_api)
            session.commit()
            session.refresh(log_api)

        return True
