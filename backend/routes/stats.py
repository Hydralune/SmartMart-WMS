from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.inventory import Inventory
from models.product import Product
from models.inbound import InboundOrder
from models.outbound import OutboundOrder
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/inventory', methods=['GET'])
@jwt_required()
def inventory_stats():
    rows = db.session.query(
        Product.category,
        func.sum(Inventory.quantity).label('total')
    ).join(Inventory, Product.id == Inventory.product_id)\
     .group_by(Product.category).all()
    return jsonify([{'category': r.category, 'total': int(r.total or 0)} for r in rows])

@stats_bp.route('/trend', methods=['GET'])
@jwt_required()
def trend_stats():
    since = datetime.now(timezone.utc) - timedelta(days=30)
    inbound = db.session.query(
        func.date(InboundOrder.created_at).label('date'),
        func.sum(InboundOrder.quantity).label('qty')
    ).filter(InboundOrder.created_at >= since).group_by(func.date(InboundOrder.created_at)).all()

    outbound = db.session.query(
        func.date(OutboundOrder.created_at).label('date'),
        func.sum(OutboundOrder.quantity).label('qty')
    ).filter(OutboundOrder.created_at >= since).group_by(func.date(OutboundOrder.created_at)).all()

    return jsonify({
        'inbound': [{'date': str(r.date), 'qty': int(r.qty or 0)} for r in inbound],
        'outbound': [{'date': str(r.date), 'qty': int(r.qty or 0)} for r in outbound],
    })
