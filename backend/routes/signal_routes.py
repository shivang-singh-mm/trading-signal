from flask import Blueprint, request, jsonify
from models import Signal
from db import db
from services.binance_service import get_price
from services.signal_service import validate_signal, update_status, get_roi
from datetime import datetime


signal_bp = Blueprint('signal_bp', __name__)


@signal_bp.route('/api/signals', methods=['POST'])
def create_signal():
    data = request.json

    error = validate_signal(data)

    if error:
        return jsonify({'message': error}), 400

    signal = Signal(
        symbol=data['symbol'].upper(),
        direction=data['direction'],
        entry_price=data['entry_price'],
        stop_loss=data['stop_loss'],
        target_price=data['target_price'],
        entry_time=datetime.fromisoformat(data['entry_time']),
        expiry_time=datetime.fromisoformat(data['expiry_time'])
    )

    db.session.add(signal)
    db.session.commit()

    return jsonify(signal.to_dict())


@signal_bp.route('/api/signals', methods=['GET'])
def get_signals():
    signals = Signal.query.order_by(Signal.created_at.desc()).all()

    all_data = []

    for signal in signals:
        current_price = get_price(signal.symbol)

        if current_price:
            update_status(signal, current_price)

        db.session.commit()

        left_time = signal.expiry_time - datetime.utcnow()
        secs = int(left_time.total_seconds())

        if secs < 0:
            secs = 0

        hours = secs // 3600
        mins = (secs % 3600) // 60

        item = signal.to_dict()

        item['current_price'] = current_price
        item['roi'] = get_roi(signal, current_price) if current_price else None
        item['time_remaining'] = f'{hours}h {mins}m'

        all_data.append(item)

    return jsonify(all_data)


@signal_bp.route('/api/signals/<int:id>', methods=['GET'])
def get_single_signal(id):
    signal = Signal.query.get(id)

    if not signal:
        return jsonify({'message': 'Signal not found'}), 404

    return jsonify(signal.to_dict())


@signal_bp.route('/api/signals/<int:id>', methods=['DELETE'])
def delete_signal(id):
    signal = Signal.query.get(id)

    if not signal:
        return jsonify({'message': 'Signal not found'}), 404

    db.session.delete(signal)
    db.session.commit()

    return jsonify({'message': 'Deleted'})