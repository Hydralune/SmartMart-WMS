from models import db
from datetime import datetime, timezone

class InboundOrder(db.Model):
    __tablename__ = 'inbound_orders'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    batch_no = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    expire_date = db.Column(db.Date)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    supplier = db.relationship('Supplier', backref='inbound_orders')
    product = db.relationship('Product', backref='inbound_orders')
    operator = db.relationship('User', backref='inbound_orders')

    def to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else '',
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'batch_no': self.batch_no,
            'quantity': self.quantity,
            'expire_date': str(self.expire_date) if self.expire_date else None,
            'operator': self.operator.username if self.operator else '',
            'created_at': str(self.created_at),
        }
