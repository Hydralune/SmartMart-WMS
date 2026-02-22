from models import db
from datetime import datetime, timezone

class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action_type = db.Column(db.String(50))
    detail = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    operator = db.relationship('User', backref='logs')

    def to_dict(self):
        return {
            'id': self.id,
            'operator': self.operator.username if self.operator else '',
            'action_type': self.action_type,
            'detail': self.detail,
            'created_at': str(self.created_at),
        }
