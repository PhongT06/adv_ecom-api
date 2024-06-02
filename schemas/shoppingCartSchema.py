from marshmallow import fields
from schemas import ma

class CartItemSchema(ma.Schema):
    id = fields.Integer(required=False)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)

class ShoppingCartSchema(ma.Schema):
    id = fields.Integer(required=False)
    customer_id = fields.Integer(required=True)
    cart_item = fields.Nested(CartItemSchema, required=True, many=True)

cart_item_schema = CartItemSchema()
shopping_cart_schema = ShoppingCartSchema()