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


def get_products_by_types(products_data: list[dict]) -> list[ProductType]:
    products_type_data: list[str] = []
    for product_data in products_data:
        products_type_data.append(product_data.get("type"))

    products_type: list[ProductType] = get_products(
        products_type_data=products_type_data
    )

    return products_type
