import hashlib
import sql_functions
from bot_actions import reply_profit_trade_to_channel
from time import time
def get_trade_hash(trade, trader_uid):
    """
    Get a trade hash
    """
    id_str = str(trade["symbol"]) + str(trade["leverage"]) + str(trader_uid)
    return hashlib.sha256(id_str.encode()).hexdigest()

def check_for_new_trade(stored_trades, trade_a):
    """
    Check if a trade is opened
    """
    new = True

    for trade_l in stored_trades:
        id_hash = get_trade_hash(trade_a, trade_l[11])
        if trade_l[0] == id_hash:
            new = False
            profit = sql_functions.check_for_profit(trade_l)
            if profit:
                reply_profit_trade_to_channel(trade_l[1], profit, trade_l[7], trade_l[9])
            break
        # If the trade is new but the timestamp is older than 5 minutes (trade timestamp minus now), ignore it
        elif trade_a["timestamp"] < (time() - 300):
            new = False
    return new

def check_for_closed_trade(api_trades, stored_trade):
    """
    Check if a trade is closed
    """
    closed = True
    for trade in api_trades:
        id_hash = get_trade_hash(trade, stored_trade[11])
        if id_hash == stored_trade[0]:
            closed = False
            sql_functions.update_trade(trade, stored_trade[0])
            break
    return closed