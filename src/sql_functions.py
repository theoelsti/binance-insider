import mysql.connector
import hashlib
# Connect to the database
conn = mysql.connector.connect(
  host="localhost",
  user="prod",
  password="rBAduV01020%65h$RVZ^q98y0MyI1",
  database="binance_insider"
)

def insert_trader(id,name):
   """
   Insert trader uid & name into the database
   """
   conn.reconnect()
   cursor = conn.cursor()
   cursor.execute("INSERT IGNORE INTO traders (uid,name) VALUES (%s,%s)",(id,name))
   conn.commit()

def insert_trade(trade,trader_uid,msg_id):
    """
    Insert trade into the database
    """
    conn.reconnect()
    cursor = conn.cursor()

    id_str = trade['symbol'] + str(trade['leverage'])
    id_hash = hashlib.sha256(id_str.encode()).hexdigest()

    query = "INSERT INTO trades (id, symbol, entry_price, mark_price, pnl, roe, amount, update_timestamp, leverage, type, trader_uid,telegram_message_id) VALUES ('{}', '{}', {}, {}, {}, {}, {}, '{}', {}, {}, '{}',{})".format(id_hash, trade['symbol'], trade['entryPrice'], trade['markPrice'], trade['pnl'], trade['roe'], trade['amount'], trade['updateTimeStamp'], trade['leverage'], 1 if trade['amount'] > 0 else 0, trader_uid,msg_id)
    cursor.execute(query)
    conn.commit()

def get_trades(trader_uid):
    """
    Get all trades for a trader from the database
    """
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades WHERE trader_uid = '{}'".format(trader_uid))
    return cursor.fetchall()