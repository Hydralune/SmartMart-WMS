from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import jwt_required
from models.log import OperationLog
from models.inventory import Inventory
from models.product import Product
from models import db
from utils.auth_decorator import role_required
import openpyxl, io

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('', methods=['GET'])
@jwt_required()
def list_logs():
    logs = OperationLog.query.order_by(OperationLog.created_at.desc()).limit(200).all()
    return jsonify([l.to_dict() for l in logs])

@logs_bp.route('/backup/export', methods=['GET'])
@role_required('admin')
def export_backup():
    wb = openpyxl.Workbook()

    # 库存 sheet
    ws1 = wb.active
    ws1.title = '库存'
    ws1.append(['商品ID', '商品名', '批次', '数量', '保质期', '货架'])
    rows = db.session.query(Inventory, Product).join(Product, Inventory.product_id == Product.id).all()
    for inv, prod in rows:
        ws1.append([prod.id, prod.name, inv.batch_no, inv.quantity, str(inv.expire_date or ''), inv.location or ''])

    # 操作日志 sheet
    ws2 = wb.create_sheet('操作日志')
    ws2.append(['操作人', '操作类型', '详情', '时间'])
    for log in OperationLog.query.order_by(OperationLog.created_at.desc()).all():
        ws2.append([
            log.operator.username if log.operator else '',
            log.action_type, log.detail, str(log.created_at)
        ])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, download_name='smartmart_backup.xlsx',
                     as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
