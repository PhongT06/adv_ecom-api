from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.customer import Customer
from models.product import Product
from models.order import Order
from datetime import datetime, timedelta

def save(order_data):
    with Session(db.engine) as session:
        with session.begin():
            # Get all of the product_ids from the order_data products
            product_ids = [prod['id'] for prod in order_data['products']]
            product_query = select(Product).where(Product.id.in_(product_ids))
            products = session.execute(product_query).scalars().all()

            # Make sure all of the products exist and were queried
            if len(product_ids) != len(products):
                raise ValueError("One or more products do not exist")
            
            # Check that the customer_id is associated with a customer
            customer_id = order_data['customer_id']
            customer = session.get(Customer, customer_id)

            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")

            # Create a new order in the database
            new_order = Order(customer_id=order_data['customer_id'], products=products)
            session.add(new_order)
            session.commit()

        session.refresh(new_order)

        for product in new_order.products:
            session.refresh(product)

        return new_order


def find_all():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders

def find_by_id(order_id):
    return db.session.get(Order, order_id)

def find_by_customer(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return orders

def get_order_status(order):
    current_date = datetime.now().date()
    order_date = order.date

    if current_date < order_date:
        return "Pending"
    elif current_date == order_date:
        return "Processing"
    elif current_date > order_date:
        if current_date <= order_date + timedelta(days=2):
            return "Shipped"
        else:
            return "Delivered"