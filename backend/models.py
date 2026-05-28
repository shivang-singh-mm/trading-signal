from db import db
from datetime import datetime


class Signal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(30), nullable=False)
    direction = db.Column(db.String(10), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    stop_loss = db.Column(db.Float, nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='OPEN')
    realized_roi = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'direction': self.direction,
            'entry_price': self.entry_price,
            'stop_loss': self.stop_loss,
            'target_price': self.target_price,
            'entry_time': self.entry_time.isoformat(),
            'expiry_time': self.expiry_time.isoformat(),
            'status': self.status,
            'realized_roi': round(self.realized_roi, 2) if self.realized_roi is not None else None,
            'created_at': self.created_at.isoformat()
        }