from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    items: Mapped[List['CartItem']] = db.relationship(back_populates='shopping_cart')

class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    shopping_cart_id: Mapped[int] = mapped_column(db.ForeignKey('shopping_carts.id'), nullable=False)
    shopping_cart: Mapped['ShoppingCart'] = db.relationship(back_populates='items')