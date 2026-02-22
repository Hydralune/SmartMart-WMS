from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import get_jwt
from models import db
from models.stocktake import StocktakeOrder
from models.inventory import Inventory
from models.log import OperationLog
from utils.auth_decorator import role_required

stocktake_bp = Blueprint('stocktake', __name__)

@stocktake_bp.route('', methods=['GET'])
@role_required('admin', 'warehouse')
def list_stocktake():
    orders = StocktakeOrder.query.order_by(StocktakeOrder.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@stocktake_bp.route('', methods=['POST'])
@role_required('admin', 'warehouse')
def create_stocktake():
    data = request.get_json()
    claims = get_jwt()
    operator_id = int(claims.get('sub') or 0)
    product_id = data['product_id']

    # 获取账面库存
    book_qty = db.session.query(db.func.sum(Inventory.quantity)).filter_by(product_id=product_id).scalar() or 0
    actual_qty = data['actual_qty']

    order = StocktakeOrder(
        product_id=product_id,
        book_qty=book_qty,
        actual_qty=actual_qty,
        diff=actual_qty - book_qty,
        operator_id=operator_id,
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@stocktake_bp.route('/<int:oid>/approve', methods=['PUT'])
@role_required('admin')
def approve_stocktake(oid):
    claims = get_jwt()
    operator_id = int(claims.get('sub') or 0)
    order = db.session.get(StocktakeOrder, oid) or abort(404)
    if order.status == 'approved':
        return jsonify({'msg': '已审核'}), 400

    # 调整库存：将该商品所有批次库存按比例调整为实际值
    invs = Inventory.query.filter_by(product_id=order.product_id).all()
    if invs:
        # 简单处理：将差值加到第一条库存记录
        invs[0].quantity += order.diff

    order.status = 'approved'
    log = OperationLog(
        operator_id=operator_id, action_type='盘点审核',
        detail=f"商品ID {order.product_id} 盘点审核通过，差异 {order.diff}"
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(order.to_dict())
