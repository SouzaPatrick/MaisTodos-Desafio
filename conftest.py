import pytest
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app import create_app


@pytest.fixture(name="engine")
def engine_fixture():  #
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def app(engine):
    app = create_app(engine_db=engine)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
