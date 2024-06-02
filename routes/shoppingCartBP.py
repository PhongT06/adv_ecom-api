from flask import Blueprint
from controllers.shoppingCartController import add_item_to_cart, remove_item_from_cart, update_item_quantity, get_shopping_cart, empty_shopping_cart, create_shopping_cart

shopping_cart_blueprint = Blueprint('shopping_cart_bp', __name__)
shopping_cart_blueprint.route('/add-item', methods=['POST'])(add_item_to_cart)
shopping_cart_blueprint.route('/remove-item', methods=['DELETE'])(remove_item_from_cart)
shopping_cart_blueprint.route('/update-quantity', methods=['PUT'])(update_item_quantity)
shopping_cart_blueprint.route('/<int:customer_id>', methods=['GET'])(get_shopping_cart)
shopping_cart_blueprint.route('/empty', methods=['DELETE'])(empty_shopping_cart)
shopping_cart_blueprint.route('/create', methods=['POST'])(create_shopping_cart)