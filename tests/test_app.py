from typing import NoReturn

from app.models import ProductType
from app_old import cashback_calculate


def test_cashback_calculate(mocker) -> NoReturn:
    products_data: list[dict] = [
        {"type": "A", "value": 10.00, "qty": 1},
        {"type": "C", "value": 10.00, "qty": 9},
    ]
    mocker.patch(
        "app_old.get_products_by_types",
        return_value=[
            ProductType(cashback_percentage=10, name="A", id=1),
            ProductType(cashback_percentage=30, name="C", id=3),
        ],
    )
    cashback: float = cashback_calculate(products_data)
    assert cashback == 28.0
