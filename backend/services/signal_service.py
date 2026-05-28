from datetime import datetime, timedelta


FINAL_STATUS = ['TARGET_HIT', 'STOPLOSS_HIT', 'EXPIRED']


def validate_signal(data):
    direction = data.get('direction')
    entry_price = float(data.get('entry_price'))
    stop_loss = float(data.get('stop_loss'))
    target_price = float(data.get('target_price'))

    entry_time = datetime.fromisoformat(data.get('entry_time'))
    expiry_time = datetime.fromisoformat(data.get('expiry_time'))

    if expiry_time <= entry_time:
        return 'Expiry time must be after entry time'

    old_limit = datetime.utcnow() - timedelta(hours=24)

    if entry_time < old_limit:
        return 'Entry time can only be 24 hours old'

    if direction == 'BUY':
        if stop_loss >= entry_price:
            return 'Stop loss must be less than entry price'

        if target_price <= entry_price:
            return 'Target price must be greater than entry price'

    if direction == 'SELL':
        if stop_loss <= entry_price:
            return 'Stop loss must be greater than entry price'

        if target_price >= entry_price:
            return 'Target price must be less than entry price'

    return None


def get_roi(signal, current_price):
    if signal.direction == 'BUY':
        roi = ((current_price - signal.entry_price) / signal.entry_price) * 100
    else:
        roi = ((signal.entry_price - current_price) / signal.entry_price) * 100

    return round(roi, 2)


def update_status(signal, current_price):
    if signal.status in FINAL_STATUS:
        return

    now = datetime.utcnow()

    if now > signal.expiry_time:
        signal.status = 'EXPIRED'
        return

    if signal.direction == 'BUY':
        if current_price >= signal.target_price:
            signal.status = 'TARGET_HIT'
            signal.realized_roi = get_roi(signal, current_price)

        elif current_price <= signal.stop_loss:
            signal.status = 'STOPLOSS_HIT'
            signal.realized_roi = get_roi(signal, current_price)

    else:
        if current_price <= signal.target_price:
            signal.status = 'TARGET_HIT'
            signal.realized_roi = get_roi(signal, current_price)

        elif current_price >= signal.stop_loss:
            signal.status = 'STOPLOSS_HIT'
            signal.realized_roi = get_roi(signal, current_price)