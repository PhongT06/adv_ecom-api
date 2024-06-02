# from flask_httpauth import HTTPTokenAuth
# from utils.util import decode_token
# from services import customerService


# token_auth = HTTPTokenAuth()


# @token_auth.verify_token
# def verify(token):
#     customer_id = decode_token(token)
#     if customer_id:
#         return customerService.get_customer(customer_id)
#     else:
#         return None

# @token_auth.error_handler
# def handle_error(status_code):
#     return {"error": "Invalid Token. Please try again"}, status_code

# @token_auth.get_user_roles
# def get_roles(customer):
#     return [customer.role.role_name]



from flask_httpauth import HTTPTokenAuth
from utils.util import decode_token
from services import customerService


token_auth = HTTPTokenAuth('Bearer')

@token_auth.verify_token
def verify_token(token):
    customer_id = decode_token(token)
    return customerService.get_customer(customer_id) if customer_id else None

@token_auth.error_handler
def auth_error():
    return {"error": "Invalid Token. Please try again"}, 401

@token_auth.get_user_roles
def get_roles(customer):
    return [customer.role.role_name] if customer else []


# from flask import current_app
# from functools import wraps
# from flask_httpauth import HTTPTokenAuth
# from utils.util import decode_token

# token_auth = HTTPTokenAuth()

# @token_auth.verify_token
# def verify_token(token):
#     customer_id = decode_token(token)
#     if customer_id is not None:
#         current_app.customer_id = customer_id
#         return True
#     return False

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not current_app.customer_id:
#             return {'message': 'Token is missing'}, 401
#         return f(*args, **kwargs)
#     return decorated

# @token_auth.error_handler
# def unauthorized():
#     return {'message': 'Unauthorized access'}, 401