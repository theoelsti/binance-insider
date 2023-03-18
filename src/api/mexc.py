import requests
from auto_trade.config import BASE_URL
from json import dumps

def get_contract_details(symbol):
    endpoint = '/v1/contract/detail'
    url = BASE_URL + endpoint
    params = {'symbol': symbol}
    response = requests.get(url, params=dumps(params))
    return(response.json())