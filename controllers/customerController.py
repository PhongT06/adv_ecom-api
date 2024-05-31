from flask import request, jsonify
from schemas.customerSchema import customer_input_schema, customer_output_schema, customers_schema, customer_login_schema, customer_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache


def save():
    try:
        # Validate and deserialize the request data
        customer_data = customer_input_schema.load(request.json)
        customer_save = customerService.save(customer_data)
        return customer_output_schema.jsonify(customer_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400



# @cache.cached(timeout=60)
def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    customers = customerService.find_all(page, per_page)
    return customers_schema.jsonify(customers), 200


def get_token():
    try:
        customer_data = customer_login_schema.load(request.json)
        token = customerService.get_token(customer_data['username'], customer_data['password'])
        if token:
            resp = {
                "status": "success",
                "message": "You have successfully authenticated yourself",
                "token": token
            }
            return jsonify(resp), 200
        else:
            resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
            return jsonify(resp), 401 # 401 - HTTP Status - Unauthorized
    except ValidationError as err:
        return jsonify(err.messages), 400


def get_customer(customer_id):
    customer = customerService.get_customer(customer_id)
    if customer:
        return customer_output_schema.jsonify(customer)
    else:
        resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
        return jsonify({'error': f'A customer with ID {customer_id} does not exist'}), 404

def update(customer_id):
    try:
        customer_data = customer_schema.load(request.json, partial=True)
        updated_customer = customerService.update(customer_id, customer_data)
        if updated_customer:
            return customer_schema.jsonify(updated_customer), 200
        else:
            return jsonify({'error': 'Customer not found'}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400

def delete(customer_id):
    deleted = customerService.delete(customer_id)
    if deleted:
        return jsonify({'message': 'Customer deleted successfully'}), 200
    else:
        return jsonify({'error': 'Customer not found'}), 404