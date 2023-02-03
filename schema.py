from datetime import datetime
from typing import NoReturn

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from marshmallow import post_load, validates
from marshmallow.exceptions import ValidationError

from person_docs_helper import validate_cpf

ma = Marshmallow()


class CustomerSchema(ma.Schema):
    document = fields.Str(required=True)
    name = fields.Str(required=True)

    class Meta:
        fields = (
            "document",
            "name",
        )

    @validates("document")
    def validate_document(self, document):
        if not validate_cpf(document):
            raise ValidationError({"error_message": "Invalid document number"})
        return document


class ProductSchema(ma.Schema):
    type = fields.Str(required=True)
    value = fields.Float(required=True)
    qty = fields.Int(required=True)

    class Meta:
        fields = (
            "type",
            "value",
            "qty",
        )


class CashbackSchema(ma.Schema):
    sold_at = fields.DateTime(required=False)
    customer = fields.Nested(CustomerSchema)
    total = fields.Float(required=True)
    products = fields.Nested(ProductSchema, many=True)

    class Meta:
        fields = (
            "sold_at",
            "customer",
            "total",
            "products",
        )

    @validates("sold_at")
    def validate_sold_at(self, sold_at):
        if datetime.now() < sold_at:
            raise ValidationError(
                {
                    "error_message": "The date entered cannot be accepted as it is in the future"
                }
            )
        return sold_at

    @post_load
    def validate(self, data, **kwargs) -> NoReturn:
        total_products: float = 0.0
        products: dict = data.get("products")
        for product in products:
            total_products += float(product.get("value") * product.get("qty"))

        if total_products != data.get("total"):
            raise ValidationError(
                {
                    "error_message": "The total value informed is not in accordance "
                    "with the value of the sum of the products sold"
                }
            )


def configure_app(app) -> NoReturn:
    ma.init_app(app)
