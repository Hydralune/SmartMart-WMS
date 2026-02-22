from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt
from models import db
from models.inbound import InboundOrder
from models.inventory import Inventory
from models.log import OperationLog
from utils.auth_decorator import role_required
from datetime import datetime, date

inbound_bp = Blueprint('inbound', __name__)

@inbound_bp.route('', methods=['GET'])
@role_required('admin', 'warehouse')
def list_inbound():
    orders = InboundOrder.query.order_by(InboundOrder.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@inbound_bp.route('', methods=['POST'])
@role_required('admin', 'warehouse')
def create_inbound():
    data = request.get_json()
    claims = get_jwt()
    operator_id = int(claims.get('sub') or 0)

    def parse_date(val):
        if not val:
            return None
        if isinstance(val, date):
            return val
        return datetime.strptime(val, '%Y-%m-%d').date()

    expire = parse_date(data.get('expire_date'))

    order = InboundOrder(
        supplier_id=data['supplier_id'],
        product_id=data['product_id'],
        batch_no=data.get('batch_no'),
        quantity=data['quantity'],
        expire_date=expire,
        operator_id=operator_id,
    )
    db.session.add(order)

    # 更新库存
    inv = Inventory.query.filter_by(
        product_id=data['product_id'], batch_no=data.get('batch_no')
    ).first()
    if inv:
        inv.quantity += data['quantity']
    else:
        inv = Inventory(
            product_id=data['product_id'],
            batch_no=data.get('batch_no'),
            quantity=data['quantity'],
            expire_date=expire,
            location=data.get('location'),
        )
        db.session.add(inv)

    # 记录日志
    log = OperationLog(
        operator_id=operator_id,
        action_type='入库',
        detail=f"商品ID {data['product_id']} 入库 {data['quantity']} 件，批次 {data.get('batch_no')}"
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(order.to_dict()), 201
