from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

# Create database engine
engine = create_engine("sqlite:///database.db")


class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cashback_percentage: int


# Create the database
SQLModel.metadata.create_all(engine)
