from typing import NoReturn, Optional

from flask import current_app
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, col, select

from .models import ProductType, User


def create_products_type_from_propulate_db() -> NoReturn:
    products_type: list[ProductType] = [
        ProductType(name="A", cashback_percentage=10),
        ProductType(name="B", cashback_percentage=20),
        ProductType(name="C", cashback_percentage=30),
    ]

    with Session(current_app.engine) as session:
        for product_type in products_type:
            session.add(product_type)
            session.commit()


def create_user_test() -> User:
    user: User = User(username="maistodos", send_cashback=True)
    user.generate_password("maistodos")

    with Session(current_app.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def exist_product_type(type: str) -> bool:
    query = select(ProductType.name)
    with Session(current_app.engine) as session:
        result = session.execute(query).scalars().all()

    if type in result:
        return True
    return False


def get_products(products_type_data: list[str]) -> list[ProductType]:
    query = select(ProductType).where(col(ProductType.name).in_(products_type_data))
    with Session(current_app.engine) as session:
        result = session.execute(query).scalars().all()

    return result


def get_products_by_types(products_data: list[dict]) -> list[ProductType]:
    products_type_data: list[str] = []
    for product_data in products_data:
        products_type_data.append(product_data.get("type"))

    products_type: list[ProductType] = get_products(
        products_type_data=products_type_data
    )

    return products_type


def get_user_by_username(username) -> Optional[User]:
    query = select(User).where(User.username == username)

    try:
        with Session(current_app.engine) as session:
            result: Optional[User] = session.execute(query).scalars().one()
    except NoResultFound:
        result: Optional[User] = None

    return result
