from app.db_function import get_products_by_types
from app.models import ProductType


def cashback_calculate(products_data: list[dict]) -> float:
    products_type: list[ProductType] = get_products_by_types(products_data)

    cashback: float = 0.0
    for product_data in products_data:
        for product_type in products_type:
            if product_data.get("type") == product_type.name:
                cashback: float = cashback + (
                    (product_data.get("value") * product_data.get("qty"))
                    * product_type.cashback_percentage
                    / 100
                )
    return cashback
