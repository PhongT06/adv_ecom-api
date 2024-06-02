from models.shoppingCart import ShoppingCart, CartItem
from database import db
from sqlalchemy.orm import Session, joinedload



def add_item_to_cart(customer_id, product_id, quantity):
    shopping_cart = db.session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
    if not shopping_cart:
        shopping_cart = ShoppingCart(customer_id=customer_id)
        db.session.add(shopping_cart)
        db.session.flush()  # Ensure the shopping_cart is persisted and has an ID

    cart_item = db.session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(product_id=product_id, quantity=quantity, shopping_cart_id=shopping_cart.id)
        db.session.add(cart_item)

    db.session.commit()  # Commit the changes to the database
    return shopping_cart

def create_cart(customer_id):
    shopping_cart = ShoppingCart(customer_id=customer_id)
    db.session.add(shopping_cart)
    db.session.commit()
    return shopping_cart

def remove_item_from_cart(customer_id, product_id):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            cart_item = session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
            if cart_item:
                session.delete(cart_item)
                session.commit()
                session.refresh(shopping_cart) 

def update_item_quantity(customer_id, product_id, quantity):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            cart_item = session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity = int(quantity)
                session.commit()
                session.refresh(shopping_cart) 

def get_shopping_cart(customer_id):
    shopping_cart = db.session.query(ShoppingCart).options(joinedload('cart_item')).filter_by(customer_id=customer_id).first()
    return shopping_cart

def empty_shopping_cart(customer_id):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id).delete()
            session.commit()
            session.refresh(shopping_cart)