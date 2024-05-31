from flask import Blueprint
from controllers.orderController import save, find_all, find_by_id, track_order, order_history


order_blueprint = Blueprint('order_bp', __name__)



order_blueprint.route('/', methods=['POST'])(save)
order_blueprint.route('/', methods=['GET'])(find_all)
order_blueprint.route('/<int:order_id>', methods=['GET'])(find_by_id)
order_blueprint.route('/<int:order_id>/track', methods=['GET'])(track_order)
order_blueprint.route('/history', methods=['GET'])(order_history)