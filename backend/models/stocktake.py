from models import db
from datetime import datetime, timezone

class StocktakeOrder(db.Model):
    __tablename__ = 'stocktake_orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    book_qty = db.Column(db.Integer, nullable=False)
    actual_qty = db.Column(db.Integer, nullable=False)
    diff = db.Column(db.Integer)
    status = db.Column(db.Enum('pending', 'approved'), default='pending')
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    product = db.relationship('Product', backref='stocktake_orders')
    operator = db.relationship('User', backref='stocktake_orders')

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'book_qty': self.book_qty,
            'actual_qty': self.actual_qty,
            'diff': self.diff,
            'status': self.status,
            'operator': self.operator.username if self.operator else '',
            'created_at': str(self.created_at),
        }
