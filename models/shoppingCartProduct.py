# from database import db, Base
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from typing import List


# class ShoppingCart(Base):
#     __tablename__ = 'carts'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
#     customer: Mapped["Customer"] = relationship(back_populates='shopping_cart')
    
#     products: Mapped[List["Product"]] = relationship('Product', secondary='cart_product', back_populates='carts')