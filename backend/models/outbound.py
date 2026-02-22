from models import db
from datetime import datetime, timezone

class OutboundOrder(db.Model):
    __tablename__ = 'outbound_orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(50))
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    product = db.relationship('Product', backref='outbound_orders')
    operator = db.relationship('User', backref='outbound_orders')

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'quantity': self.quantity,
            'department': self.department,
            'operator': self.operator.username if self.operator else '',
            'created_at': str(self.created_at),
        }
