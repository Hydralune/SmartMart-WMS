from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.supplier import Supplier
from utils.auth_decorator import role_required

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('', methods=['GET'])
@jwt_required()
def list_suppliers():
    return jsonify([s.to_dict() for s in Supplier.query.all()])

@suppliers_bp.route('', methods=['POST'])
@role_required('admin', 'purchaser')
def create_supplier():
    data = request.get_json()
    s = Supplier(
        name=data['name'], contact=data.get('contact'),
        phone=data.get('phone'), category=data.get('category'),
        status=data.get('status', 'active')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@suppliers_bp.route('/<int:sid>', methods=['PUT'])
@role_required('admin', 'purchaser')
def update_supplier(sid):
    s = Supplier.query.get_or_404(sid)
    data = request.get_json()
    for field in ['name', 'contact', 'phone', 'category', 'status']:
        if field in data:
            setattr(s, field, data[field])
    db.session.commit()
    return jsonify(s.to_dict())

@suppliers_bp.route('/<int:sid>', methods=['DELETE'])
@role_required('admin')
def delete_supplier(sid):
    s = Supplier.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'msg': '删除成功'})
