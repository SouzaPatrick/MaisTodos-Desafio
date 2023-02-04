from datetime import datetime
from typing import Optional

from flask_marshmallow.fields import fields
from marshmallow import post_load, validates
from marshmallow.exceptions import ValidationError

from app import ma
from person_docs_helper import remove_mask_cpf, validate_cpf

from .db_function import exist_product_type

# ma = Marshmallow()


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
        return remove_mask_cpf(document)


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

    @validates("type")
    def validate_type(self, type: str):
        if not exist_product_type(type=type):
            raise ValidationError(
                {"error_message": f"The {type} product type is invalid"}
            )
        return type


class CashbackSchema(ma.Schema):
    sold_at = fields.DateTime(required=False)
    customer = fields.Nested(CustomerSchema, required=True)
    total = fields.Float(required=True)
    products = fields.Nested(ProductSchema, many=True, required=True)

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
    def validate(self, data, **kwargs) -> Optional[dict]:
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

        return data
