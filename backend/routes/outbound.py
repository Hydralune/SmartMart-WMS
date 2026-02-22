from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt
from models import db
from models.outbound import OutboundOrder
from models.inventory import Inventory
from models.log import OperationLog
from utils.auth_decorator import role_required

outbound_bp = Blueprint('outbound', __name__)

@outbound_bp.route('', methods=['GET'])
@role_required('admin', 'warehouse')
def list_outbound():
    orders = OutboundOrder.query.order_by(OutboundOrder.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@outbound_bp.route('', methods=['POST'])
@role_required('admin', 'warehouse')
def create_outbound():
    data = request.get_json()
    claims = get_jwt()
    operator_id = int(claims.get('sub') or 0)
    product_id = data['product_id']
    qty = data['quantity']

    # 校验库存
    total = db.session.query(db.func.sum(Inventory.quantity)).filter_by(product_id=product_id).scalar() or 0
    if total < qty:
        return jsonify({'msg': f'库存不足，当前库存 {total}'}), 400

    # 扣减库存（按批次先进先出）
    remaining = qty
    for inv in Inventory.query.filter_by(product_id=product_id).order_by(Inventory.expire_date).all():
        if remaining <= 0:
            break
        deduct = min(inv.quantity, remaining)
        inv.quantity -= deduct
        remaining -= deduct

    order = OutboundOrder(
        product_id=product_id, quantity=qty,
        department=data.get('department'), operator_id=operator_id
    )
    db.session.add(order)

    log = OperationLog(
        operator_id=operator_id, action_type='出库',
        detail=f"商品ID {product_id} 出库 {qty} 件，领用部门 {data.get('department')}"
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(order.to_dict()), 201
