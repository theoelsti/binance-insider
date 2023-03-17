import requests
import json
from time import sleep
import sql_functions as sql
import errors_printing as errors
HEADERS = {
        'Content-Type': 'application/json'
    }

def get_top_traders(x,trade_type="PERPETUAL"):
    """
    Returns a list of the top x traders on Binance Futures. 
    """

    traders = []
    url = "https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank"
    payload = {
        "isShared": True,
        "isTrader": False,
        "periodType": "MONTHLY",
        "statisticsType": "ROI",
        "tradeType": trade_type
    }
    headers = HEADERS

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response = response.json()['data']
    for trader in response[:x]:
        traders.append([trader['encryptedUid'],  trader['nickName']])
    return traders

def get_trader_trades(trader_uid, trade_type="PERPETUAL"):
    """
    Returns a list of trades for a given UID under JSON Format.
    """
    url = "https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition"
    payload = {
        "encryptedUid": trader_uid,
        "tradeType": trade_type
    }
    headers = HEADERS
    try: 
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload)) 
    except Exception as e:
        errors.print_error("Error while fetching trades for trader : " + trader_uid)
        errors.print_error(e)
        
    if(response.status_code != 200):
        errors.print_error("Error while fetching trades for trader : " + trader_uid)
        print(response.status_code)
        sleep(10)
        return get_trader_trades(trader_uid, trade_type)
    response = response.json()['data']['otherPositionRetList']
    return response

def get_trader_infos(trader_uid):
    """
    Returns the trader infos under JSON Format.
    """
    url = "https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo"
    payload = {
        "encryptedUid": trader_uid
    }
    headers = HEADERS
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response = response.json()['data']

    query = "INSERT INTO traders (uid,name) VALUES (%s,%s)"%(response['encryptedUid'],response['nickName'])
    sql.insert(query)
    return response

def get_trader_username_api(id):
    """
    Fetch the trader username from the api
    """
    url = "https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo"
    payload = {
        "encryptedUid": id
    }
    headers = HEADERS
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response = response.json()['data']

    return response['nickName']