from marshmallow import fields
from schemas import ma


class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=False)
    customer_id = fields.Integer(required=True)
    products = fields.Nested("ProductIdSchema", required=True, many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
