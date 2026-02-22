from models import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    category = db.Column(db.String(100))
    status = db.Column(db.Enum('active', 'inactive'), default='active')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'contact': self.contact,
            'phone': self.phone, 'category': self.category, 'status': self.status
        }
