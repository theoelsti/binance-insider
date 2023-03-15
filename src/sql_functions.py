import mysql.connector
from trades import get_trade_hash
import errors_printing as errors
# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="prod",
    password="rBAduV01020%65h$RVZ^q98y0MyI1",
    database="binance_insider",
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


def delete_trade(trade_id):
    """
    Delete trade from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades WHERE id = '{}'".format(trade_id))
    conn.commit()
    # Check if well deleted
    cursor.execute("SELECT COUNT(*) FROM trades WHERE id = '{}'".format(trade_id))
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
        trade["updateTimeStamp"],
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
    cursor = cursor.execute("UPDATE trades SET mark_price= {}, pnl = {}, roe = {}, amount = {}, update_timestamp = '{}' WHERE id = '{}';".format(trade["markPrice"],trade["pnl"],trade["roe"],trade["amount"],trade["updateTimeStamp"],trade_id))
    conn.commit()
    print(cursor.rowcount, "record(s) affected")