import hashlib

def check_for_new_trade(stored_trades, trade_a):
    """
    Check if a trade is opened
    """
    new = True # A refaire totalement : Comparer le trade avec le résultat de la bdd
    
    for trade_l in stored_trades:
        id_str = str(trade_a['symbol']) + str(trade_a['leverage'])
        id_hash = hashlib.sha256(id_str.encode()).hexdigest()
        
        if trade_l[0] == id_hash:
            new = False
            break
    return new