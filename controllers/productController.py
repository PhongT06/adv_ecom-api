from flask import request, jsonify
from schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError
from auth import token_auth


@token_auth.login_required
def save():
    # logged_in_customer = token_auth.current_user()
    # print(logged_in_customer)
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = productService.save(product_data)

    return product_schema.jsonify(new_product), 201


def find_all():
    # Get any request query params aka args
    args = request.args
    page = args.get('page', 1, type=int)
    # print('The page arg is:', page, 'and the type is', type(page))
    per_page = args.get('per_page', 10, type=int)
    search_term = args.get('search')
    products = productService.find_all(page, per_page, search_term)
    return products_schema.jsonify(products)

def find_by_id(product_id):
    product = productService.get_product(product_id)
    if product:
        return product_schema.jsonify(product), 200
    else:
        return jsonify({'error': 'Product not found'}), 404

@token_auth.login_required(role="admin")
def update(product_id):
    try:
        product_data = product_schema.load(request.json, partial=True)
        updated_product = productService.update(product_id, product_data)
        if updated_product:
            return product_schema.jsonify(updated_product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400

@token_auth.login_required(role="admin")
def delete(product_id):
    deleted = productService.delete(product_id)
    if deleted:
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404