from typing import NoReturn

from flask import current_app
from sqlalchemy.future import Engine
from sqlmodel import SQLModel, create_engine


def get_engine() -> Engine:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url)

    return engine


def create_db_and_tables() -> NoReturn:
    SQLModel.metadata.create_all(current_app.engine)
