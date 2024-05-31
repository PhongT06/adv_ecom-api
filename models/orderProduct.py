from database import db


order_product = db.Table(
    "order_product",
    db.Column('product_id', db.ForeignKey('products.id'), primary_key=True),
    db.Column('order_id', db.ForeignKey('orders.id'), primary_key=True)
)
