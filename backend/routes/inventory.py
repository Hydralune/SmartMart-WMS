from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db
from models.inventory import Inventory
from utils.auth_decorator import role_required

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('', methods=['GET'])
@jwt_required()
def list_inventory():
    q = request.args.get('q', '')
    category = request.args.get('category', '')
    items = Inventory.query.join(Inventory.product)
    if q:
        from models.product import Product
        items = items.filter(Product.name.ilike(f'%{q}%'))
    if category:
        from models.product import Product
        items = items.filter(Product.category == category)
    return jsonify([i.to_dict() for i in items.all()])
