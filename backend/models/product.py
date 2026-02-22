from models import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    spec = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    stock_min = db.Column(db.Integer, default=0)
    stock_max = db.Column(db.Integer, default=9999)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'category': self.category,
            'spec': self.spec, 'unit': self.unit,
            'stock_min': self.stock_min, 'stock_max': self.stock_max
        }
