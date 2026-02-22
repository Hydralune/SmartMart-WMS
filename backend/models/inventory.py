from models import db
from datetime import date

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    batch_no = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)
    expire_date = db.Column(db.Date)
    location = db.Column(db.String(50))

    product = db.relationship('Product', backref='inventory_items')

    def days_until_expire(self):
        if self.expire_date:
            return (self.expire_date - date.today()).days
        return None

    def to_dict(self):
        p = self.product
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': p.name if p else '',
            'category': p.category if p else '',
            'spec': p.spec if p else '',
            'unit': p.unit if p else '',
            'batch_no': self.batch_no,
            'quantity': self.quantity,
            'expire_date': str(self.expire_date) if self.expire_date else None,
            'days_until_expire': self.days_until_expire(),
            'location': self.location,
            'stock_min': p.stock_min if p else 0,
            'stock_max': p.stock_max if p else 9999,
        }
