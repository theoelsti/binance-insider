import requests
import json
import time
import sqlFunctions as sql

def get_top_traders(x,trade_type="PERPETUAL"):
    """
    Returns a list of the top x traders on Binance Futures. 
    """

    traders = []
    url = "https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank"
    payload = {
        "isShared": True,
        "isTrader": True,
        "periodType": "MONTHLY",
        "statisticsType": "ROI",
        "tradeType": trade_type
    }
    headers = {
        'Content-Type': 'application/json'
    }
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
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
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
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response = response.json()['data']

    query = "INSERT INTO traders (uid,name) VALUES (%s,%s)"%(response['encryptedUid'],response['nickName'])
    sql.insert(query)
    return response