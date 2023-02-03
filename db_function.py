from sqlmodel import Session, select

from models import ProductType, engine


def exist_product_type(type: str) -> bool:
    query = select(ProductType.nome)
    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    if type in result:
        return True
    return False
