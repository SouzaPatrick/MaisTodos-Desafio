from sqlmodel import Session, col, select

from models import ProductType, engine


def exist_product_type(type: str) -> bool:
    query = select(ProductType.name)
    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    if type in result:
        return True
    return False


def get_products(products_type_data: list[str]) -> list[ProductType]:
    query = select(ProductType).where(col(ProductType.name).in_(products_type_data))
    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    return result
