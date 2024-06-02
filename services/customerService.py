from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.customer import Customer
from circuitbreaker import circuit
from werkzeug.security import generate_password_hash, check_password_hash
from utils.util import encode_token


# Fallback function - executed once the limit has been passed
def fallback_func(customer_data):
    print('The fallback function is being executed')
    return None

# Create a function that takes in customer data and creates a new customer in db
def save(customer_data):
    # Open a session
    with Session(db.engine) as session:
        with session.begin():
            # Check to see if any customer has that username
            customer_query = select(Customer).where(Customer.username == customer_data['username'])
            customer_check = session.execute(customer_query).scalars().first()
            # If we do find a customer with that username, raise a ValueError
            if customer_check is not None:
                raise ValueError("Customer with that username already exists")
            # Create a new instance of Customer
            new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], username=customer_data['username'], password=generate_password_hash(customer_data['password']))
            # Add and commit to the database
            session.add(new_customer)
            session.commit()
        # After committing the session, the new_customer object may have become detatched
        # Refresh the object to ensure it is still attached to the session
        session.refresh(new_customer)
        return new_customer


# Function to get all of the customers from the db
def find_all(page=1, per_page=10):
    query = db.select(Customer).offset((page-1) * per_page).limit(per_page)
    customers = db.session.execute(query).scalars().all()
    return customers


# Function that will take in a username and password and return token if valid, None if not
def get_token(username, password):
    # Query the customer table for that username
    query = db.select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalars().first()
    if customer is not None and check_password_hash(customer.password, password):
        # Create a token with the customer's id
        auth_token = encode_token(customer.id)
        return auth_token
    else:
        return None

# Function that will take in a customer id and return than customer or None
def get_customer(customer_id):
    return db.session.get(Customer, customer_id)


def update(customer_id, customer_data):
    with Session(db.engine) as session:
        customer = session.get(Customer, customer_id)
        if customer:
            for key, value in customer_data.items():
                setattr(customer, key, value)
            session.commit()
            session.refresh(customer)
            return customer
    return None



def delete(customer_id):
    with Session(db.engine) as session:
        customer = session.get(Customer, customer_id)
        if customer:
            session.delete(customer)
            session.commit()
            return True
    return False