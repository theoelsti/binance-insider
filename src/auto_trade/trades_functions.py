import requests
import json
import hmac
import hashlib
import time

from config import API_KEY, SECRET_KEY

def get_signature(secret_key, message):
    return hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

def place_future_order(symbol, side, quantity, price, leverage, order_type='LIMIT'):
    base_url = 'https://api.mexc.com'
    endpoint = '/v1/contract/order'
    url = base_url + endpoint

    timestamp = int(time.time() * 1000)
    params = {
        'api_key': API_KEY,
        'req_time': timestamp,
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'price': price,
        'volume': quantity,
        'leverage': leverage
    }

    pre_sign = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = get_signature(SECRET_KEY, pre_sign)
    params['sign'] = signature

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(params), headers=headers)

    return response.json()

symbol = 'BTC_USDT'
side = 'BUY'  # Choisir entre 'BUY' et 'SELL'
quantity = 1
price = 50000
leverage = 10

response = place_future_order(symbol, side, quantity, price, leverage)
print(response)
