import hashlib


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
            break
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
            break
    return closed
