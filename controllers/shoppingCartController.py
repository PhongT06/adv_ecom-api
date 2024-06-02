from flask import request, jsonify
from schemas.shoppingCartSchema import shopping_cart_schema, cart_item_schema
from services import shoppingCartService
from services.shoppingCartService import get_shopping_cart
from services.shoppingCartService import create_cart
from auth import token_auth
from database import db
from models.shoppingCart import ShoppingCart, CartItem


@token_auth.login_required
def add_item_to_cart():
    customer_id = token_auth.current_user().id
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')

    if not product_id or not quantity:
        return jsonify({'error': 'Missing product_id or quantity'}), 400
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({'error': 'Invalid quantity value'}), 400
    try:
        with db.session.begin_nested():
            shopping_cart = ShoppingCart.query.filter_by(customer_id=customer_id).first()
            if not shopping_cart:
                shopping_cart = ShoppingCart(customer_id=customer_id)
                db.session.add(shopping_cart)
                db.session.flush()
            
            cart_item = CartItem.query.filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(product_id=product_id, quantity=quantity, shopping_cart_id=shopping_cart.id)
                db.session.add(cart_item)

            db.session.commit()  # Commit the changes to the database
            return shopping_cart
        
        return shopping_cart_schema.jsonify(shopping_cart), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@token_auth.login_required
def create_shopping_cart():
    customer_id = token_auth.current_user().id
    try:
        shopping_cart = create_cart(customer_id)
        return shopping_cart_schema.jsonify(shopping_cart), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@token_auth.login_required
def remove_item_from_cart():
    customer_id = token_auth.current_user().id
    product_id = request.json.get('product_id')

    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400
    try:
        with db.session.begin_nested():
            shopping_cart = shoppingCartService.remove_item_from_cart(customer_id, product_id)
            db.session.add(shopping_cart)
        return shopping_cart_schema.jsonify(shopping_cart), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@token_auth.login_required
def update_item_quantity():
    customer_id = token_auth.current_user().id
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')

    if not product_id or not quantity:
        return jsonify({'error': 'Missing product_id or quantity'}), 400
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({'error': 'Invalid quantity value'}), 400
    try:
        with db.session.begin_nested():
            shopping_cart = shoppingCartService.update_item_quantity(customer_id, product_id, quantity)
            db.session.add(shopping_cart)
        return shopping_cart_schema.jsonify(shopping_cart), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@token_auth.login_required
def get_shopping_cart(customer_id):
    customer_id = token_auth.current_user().id
    try:
        shopping_cart = get_shopping_cart(customer_id)
        if shopping_cart:
            return shopping_cart_schema.jsonify(shopping_cart), 200
        else:
            return jsonify({'message': 'Shopping cart not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@token_auth.login_required
def empty_shopping_cart():
    customer_id = token_auth.current_user().id
    try:
        with db.session.begin_nested():
            shopping_cart = shoppingCartService.empty_shopping_cart(customer_id)
            db.session.add(shopping_cart)
        return jsonify({'message': 'Shopping cart emptied successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500