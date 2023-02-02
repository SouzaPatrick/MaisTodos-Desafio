from typing import NoReturn
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from person_docs_helper import validate_cpf
from marshmallow.exceptions import ValidationError
from marshmallow import validates

ma = Marshmallow()

class CustomerSchema(ma.Schema):
    document = fields.Str(required=True)
    name = fields.Str(required=True)

    class Meta:
        fields = (
            'document',
            'name',
        )

    @validates('document')
    def validate_document(self, document):
        if not validate_cpf(document):
            raise ValidationError({'error_message': 'Invalid document number'})
        return document


class ProductSchema(ma.Schema):
    type = fields.Str(required=True)
    value = fields.Str(required=True)
    qty = fields.Int(required=True)

    class Meta:
        fields = (
            'type',
            'value',
            'qty',
        )


class CashbackSchema(ma.Schema):
    sold_at = fields.Str(required=False)
    customer = fields.Nested(CustomerSchema)
    total = fields.Str(required=True)
    products = fields.Nested(ProductSchema, many=True)

    class Meta:
        fields = (
            'sold_at',
            'customer',
            'total',
            'products',
        )


def configure_app(app) -> NoReturn:
    ma.init_app(app)