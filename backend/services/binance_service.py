import requests


BASE_URL = 'https://api.binance.com/api/v3/ticker/price'


def get_price(symbol):
    try:
        res = requests.get(f'{BASE_URL}?symbol={symbol}')
        data = res.json()
        return float(data['price'])
    except:
        return None