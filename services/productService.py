from sqlalchemy.orm import Session
from database import db
from models.product import Product


def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            # Create a new instance of Product
            new_product = Product(name=product_data['name'], price=product_data['price'])
            # Add that instance to the db
            session.add(new_product)
            session.commit()
        session.refresh(new_product)
        return new_product


# Function to get all products from the Products table
def find_all(page=1, per_page=10, search_term=None):
    query = db.select(Product)
    if search_term:
        query = query.where(Product.name.ilike(f"%{search_term}%"))
    query = query.limit(per_page).offset((page-1)*per_page)
    products = db.session.execute(query).scalars().all()
    return products

def get_product(product_id):
    return db.session.get(Product, product_id)

def update(product_id, product_data):
    with Session(db.engine) as session:
        product = session.get(Product, product_id)
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            session.commit()
            session.refresh(product)
            return product
    return None

def delete(product_id):
    with Session(db.engine) as session:
        product = session.get(Product, product_id)
        if product:
            session.delete(product)
            session.commit()
            return True
    return False