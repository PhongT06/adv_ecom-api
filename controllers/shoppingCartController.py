from flask import request, jsonify
from schemas.shoppingCartSchema import shopping_cart_schema
from services import shoppingCartService
from auth import token_auth

# @token_auth.login_required
# def add_item_to_cart():
#     customer_id = token_auth.current_user().id
#     product_id = request.json.get('product_id')
#     quantity = request.json.get('quantity')

#     if not product_id or not quantity:
#         return jsonify({'error': 'Missing product_id or quantity'}), 400
#     try:
#         quantity = int(quantity)
#     except ValueError:
#         return jsonify({'error': 'Invalid quantity value'}), 400
#     try:
#         shoppingCartService.add_item_to_cart(customer_id, product_id, quantity)
#         shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
#         return shopping_cart_schema.jsonify(shopping_cart), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @token_auth.login_required
# def remove_item_from_cart():
#     customer_id = token_auth.current_user().id
#     product_id = request.json.get('product_id')

#     shoppingCartService.remove_item_from_cart(customer_id, product_id)
#     shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
#     return shopping_cart_schema.jsonify(shopping_cart), 200

# @token_auth.login_required
# def update_item_quantity():
#     customer_id = token_auth.current_user().id
#     product_id = request.json.get('product_id')
#     quantity = request.json.get('quantity')

#     shoppingCartService.update_item_quantity(customer_id, product_id, quantity)
#     shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
#     return shopping_cart_schema.jsonify(shopping_cart), 200

# @token_auth.login_required
# def get_shopping_cart():
#     customer_id = token_auth.current_user().id
#     shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
#     return shopping_cart_schema.jsonify(shopping_cart), 200

# @token_auth.login_required
# def empty_shopping_cart():
#     customer_id = token_auth.current_user().id
#     shoppingCartService.empty_shopping_cart(customer_id)
#     return jsonify({'message': 'Shopping cart emptied successfully'}), 200


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
        shoppingCartService.add_item_to_cart(customer_id, product_id, quantity)
        shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
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
        shoppingCartService.remove_item_from_cart(customer_id, product_id)
        shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
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
        shoppingCartService.update_item_quantity(customer_id, product_id, quantity)
        shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
        return shopping_cart_schema.jsonify(shopping_cart), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@token_auth.login_required
def get_shopping_cart():
    customer_id = token_auth.current_user().id
    try:
        shopping_cart = shoppingCartService.get_shopping_cart(customer_id)
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
        shoppingCartService.empty_shopping_cart(customer_id)
        return jsonify({'message': 'Shopping cart emptied successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500