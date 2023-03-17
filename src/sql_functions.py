import mysql.connector
from trades import get_trade_hash
import errors_printing as errors
from time import time
from contextlib import contextmanager
from api.binance import get_trader_username_api
PROFIT_TRESHOLD = 25

@contextmanager
def get_connection():
    conn = mysql.connector.connect(
        host="193.70.43.232",
        user="prod_script",
        password="rBAduV01020%65h$RVZ^q98y0MyI1",
        database="binance_insider",
        auth_plugin="mysql_native_password"
    )
    try:
        yield conn
    finally:
        conn.close()

def get_trader_username(id):
    """
    Fetch the trader username from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT name FROM traders WHERE uid = '{}'".format(id))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

def get_traders():
    """
    Fetch all traders from the database, in the format : 
    [[uid, name], [uid, name], ...]
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT uid,name FROM traders")
        return_tab = []
        for (uid, name) in cursor:
            return_tab.append([uid, name])
        return return_tab

def insert_trader_with_uid(id):
    """
    Insert a trader after fetching his name from the API
    """
    name = get_trader_username_api(id)
    insert_trader(id, name)

def insert_trader(id, name):
    """
    Insert trader uid & name into the database
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor(buffered=True)
            cursor.execute("INSERT IGNORE INTO traders (uid,name) VALUES (%s,%s)", (id, name))
            conn.commit()
    except Exception as e:
        print(e)

def count_total_trades():
    """
    Count total trades in the database
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT COUNT(*) FROM trades")
            return cursor.fetchone()[0]
    except Exception as e:
        print("Error counting trades", e)

def delete_trade(trade):
    """
    Delete trade from the database
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor(buffered=True)
            cursor.execute("DELETE FROM trades WHERE id = '{}'".format(trade[0]))
            conn.commit()
            cursor.execute("INSERT INTO daily_trades (trade_id, symbol, opened,closed, message_id, profit) VALUES ('{}','{}',{},{},{},{});".format(trade[0],trade[1],trade[7],int(time()),trade[9],trade[5]))
            cursor.execute("SELECT COUNT(*) FROM trades WHERE id = '{}'".format(trade[0]))
            conn.commit()
            return cursor.fetchone()[0] == 0
    except Exception as e:
        print(e)

def delete_trader(trader_uid):
    """
    Delete trader from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
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

    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            errors.print("Failed to insert trade into the database: " + str(e))
            raise e

def get_trades(trader_uid):
    """
    Get all trades for a trader from the database
    """
    query = "SELECT * FROM trades WHERE trader_uid = '{}'".format(trader_uid)
    try:
        with get_connection() as conn:
            cursor = conn.cursor(buffered=True)
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print("Error: {}".format(e))

def update_trade(trade, trade_id):
    """
    Update the trade in the database
    """
    query = "UPDATE trades SET mark_price= {}, pnl = {}, roe = {}, amount = {} WHERE id = '{}';".format(trade["markPrice"], trade["pnl"], trade["roe"], trade["amount"], trade_id)

    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            print("Error while updating trade: {}".format(e))
            raise

def check_for_profit(s_trade):
    """
    Check if the trade is in profit
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT roe, announced_roe FROM trades WHERE id = '{}'".format(s_trade[0]))

            result = cursor.fetchone()

            if result:
                roe = result[0]
                announced_trade = result[1]
                roe_percentage = int(roe * 100)
                if announced_trade is None:
                    announced_trade = 0
                if int(roe_percentage) > int(announced_trade) + PROFIT_TRESHOLD:
                    cursor.execute(
                        "UPDATE trades SET announced_roe = {} WHERE id = '{}'".format(
                            int(announced_trade) + PROFIT_TRESHOLD, s_trade[0]
                        )
                    )
                    conn.commit()
                    return int(announced_trade) + PROFIT_TRESHOLD
                else:
                    return 0
            else:
                return 0
    except Exception as e:
        print("Failed to check for profit: " + str(e))

def insert_token(token, type):
    """
    Insert token into the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute(
                "INSERT INTO subscription_tokens (token, subscription_type) VALUES ('{}', '{}')".format(token, type)
            )
            conn.commit()
        except Exception as e:
            print("Error: {}".format(e))

def get_tokens(type):
    """
    Get all tokens from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT token FROM subscription_tokens WHERE subscription_type = '{}'".format(type))
        conn.commit()

        tokens = cursor.fetchall()
        if not tokens:
            raise ValueError("No tokens found for type {}".format(type))
        return tokens

def get_sum_profit():
    """
    Get sum of all profits from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("""
        SELECT 
            SUM(CASE WHEN profit > 0 THEN profit ELSE 0 END) as total_positive_profit,
            SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) as total_losses
        FROM daily_trades;
        """)
        return cursor.fetchone()

def delete_daily_trades():
    """
    Delete all daily profits from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("TRUNCATE TABLE daily_trades")
        conn.commit()

def insert_daily_profit(winning,loosing,profit):
    """
    Insert daily profit into the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute(f"INSERT INTO daily_summary (profit, total_trades, winning_trades, losing_trades, date) VALUES ({profit}, {int(winning) + int(loosing)}, {int(winning)}, {int(loosing)}, CURRENT_DATE);"
)
        conn.commit()

def get_winning_losing_trades():
    """
    Get all winning and losing trades from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM daily_trades WHERE profit > 0 ORDER BY profit DESC LIMIT 3;")
        winning_trades = cursor.fetchall()
        cursor.execute("SELECT * FROM daily_trades WHERE profit < 0 ORDER BY profit ASC LIMIT 3;")
        losing_trades = cursor.fetchall()
        return [winning_trades,losing_trades]

def get_count_winning_loosing_trades():
    """
    Get count of all winning and losing trades from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT COUNT(*) FROM daily_trades WHERE profit > 0;")
        winning_trades = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM daily_trades WHERE profit < 0;")
        losing_trades = cursor.fetchone()
        return [winning_trades,losing_trades]

def get_closed_trade():
    """
    Get all closed trades from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM daily_trades;")
        return cursor.fetchall()