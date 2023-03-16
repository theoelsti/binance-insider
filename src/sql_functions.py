import mysql.connector
from trades import get_trade_hash
import errors_printing as errors
from time import time

PROFIT_TRESHOLD = 25
conn = mysql.connector.connect(
    host="193.70.43.232",
    user="prod_script",
    password="rBAduV01020%65h$RVZ^q98y0MyI1",
    database="binance_insider",
    auth_plugin="mysql_native_password"
)

def get_trader_username(id):
    """
    Fetch the trader username from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM traders WHERE uid = '{}'".format(id))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def insert_trader(id, name):
    """
    Insert trader uid & name into the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO traders (uid,name) VALUES (%s,%s)", (id, name))
    conn.commit()

def count_total_trades():
    """
    Count total trades in the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM trades")
    return cursor.fetchone()[0]

def delete_trade(trade):
    """
    Delete trade from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades WHERE id = '{}'".format(trade[0]))
    conn.commit()
    # Check if well deleted
    cursor.execute("INSERT INTO daily_trades (trade_id, symbol, opened,closed, message_id, profit) ('{}','{}',{},{},{},{})'".format(trade[0],trade[1],trade[7],int(time()),trade[9],trade[5]))
    # Insert the trade in the daily trades table
    cursor.execute("SELECT COUNT(*) FROM trades WHERE id = '{}'".format(trade[0]))
    return cursor.fetchone()[0] == 0

def delete_trader(trader_uid):
    """
    Delete trader from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades WHERE trader_uid = '{}'".format(trader_uid))
    cursor.execute("DELETE FROM traders WHERE uid = '{}'".format(trader_uid))
    conn.commit()
    # Check if well deleted
    cursor.execute("SELECT COUNT(*) FROM trades WHERE trader_uid = '{}'".format(trader_uid))
    return cursor.fetchone()[0] == 0

def insert_trade(trade, trader_uid, msg_id):
    """
    Insert trade into the database
    """
    conn.reconnect()
    cursor = conn.cursor()

    id_hash = get_trade_hash(trade, trader_uid)

    query = "INSERT INTO trades (id, symbol, entry_price, mark_price, pnl, roe, amount, update_timestamp, leverage, type, trader_uid,telegram_message_id) VALUES ('{}', '{}', {}, {}, {}, {}, {}, '{}', {}, {}, '{}',{})".format(
        id_hash,
        trade["symbol"],
        trade["entryPrice"],
        trade["markPrice"],
        trade["pnl"],
        trade["roe"],
        trade["amount"],
        time(),
        trade["leverage"],
        1 if trade["amount"] > 0 else 0,
        trader_uid,
        msg_id,
    )
    try:
        cursor.execute(query)
    except Exception as e:
        errors.print("Failed to insert trade into the database: " + str(e))

    conn.commit()

def get_trades(trader_uid):
    """
    Get all trades for a trader from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades WHERE trader_uid = '{}'".format(trader_uid))
    return cursor.fetchall()

def update_trade(trade,trade_id ):
    """
    Update the trade in the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("UPDATE trades SET mark_price= {}, pnl = {}, roe = {}, amount = {} WHERE id = '{}';".format(trade["markPrice"],trade["pnl"],trade["roe"],trade["amount"],trade_id))
    conn.commit()

def check_for_profit(s_trade):


    """
    Check if the trade is in profit
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT roe,announced_roe FROM trades WHERE id = '{}'".format(s_trade[0]))

    result = cursor.fetchone()
    
    if result:
        roe = result[0]
        announced_trade = result[1]
        roe_percentage = int(roe * 100)
        if announced_trade == None:
            announced_trade = 0
        if  int(roe_percentage) > int(announced_trade)+PROFIT_TRESHOLD:
            # Update the announced_trade value in the database.
            cursor.execute("UPDATE trades SET announced_roe = {} WHERE id = '{}'".format(int(announced_trade)+PROFIT_TRESHOLD, s_trade[0]))
            conn.commit()
            return int(announced_trade)+PROFIT_TRESHOLD
        else: 
            return 0
        
def insert_token(token,type):
    """
    Insert token into the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscription_tokens (token,subscription_type) VALUES ('{}', '{}')".format(token, type))
    conn.commit()

def get_tokens(type):
    """
    Get all tokens from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT token FROM subscription_tokens WHERE subscription_type = '{}'".format(type))
    return cursor.fetchall()