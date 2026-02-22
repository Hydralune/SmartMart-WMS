from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.product import Product
from utils.auth_decorator import role_required

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
@jwt_required()
def list_products():
    q = request.args.get('q', '')
    query = Product.query
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    return jsonify([p.to_dict() for p in query.all()])

@products_bp.route('', methods=['POST'])
@role_required('admin')
def create_product():
    data = request.get_json()
    p = Product(
        name=data['name'], category=data.get('category'),
        spec=data.get('spec'), unit=data.get('unit'),
        stock_min=data.get('stock_min', 0), stock_max=data.get('stock_max', 9999)
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@products_bp.route('/<int:pid>', methods=['PUT'])
@role_required('admin')
def update_product(pid):
    p = Product.query.get_or_404(pid)
    data = request.get_json()
    for field in ['name', 'category', 'spec', 'unit', 'stock_min', 'stock_max']:
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify(p.to_dict())

@products_bp.route('/<int:pid>', methods=['DELETE'])
@role_required('admin')
def delete_product(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'msg': '删除成功'})
