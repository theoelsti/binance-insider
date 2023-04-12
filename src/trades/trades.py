import hashlib
from time import time
from database import db_functions
from api.telegram import send_telegram_message
from messages.profit_trade_message import ProfitTradeMessage
import utils.logs as custom_logging 
from utils.config_handler import telegram_config
CALLS_CHANNEL_ID = telegram_config['calls_channel_id']

def generate_trade_hash(trade, trader_uid):
    """
    Generate a unique hash for a trade.
    
    :param trade: A dictionary containing trade information.
    :param trader_uid: A unique identifier for the trader.
    :return: A hash string representing the unique trade.
    """
    direction = 1 if trade["amount"] > 0 else 0
    id_str = str(trade["symbol"]) + str(trade["leverage"]) + str(trader_uid) + str(direction)
    return hashlib.sha256(id_str.encode()).hexdigest()


def is_trade_new(stored_trades, trade_api):
    """
    Check if a trade is opened and not already in the stored trades.

    :param stored_trades: A list of stored trades.
    :param trade_api: A dictionary containing trade information from the API.
    :return: True if the trade is new, False otherwise.
    """
    is_new = True
    difference = abs(trade_api['entryPrice'] - trade_api['markPrice'])
    percentage_difference = (difference / trade_api['entryPrice']) * 100

    for stored_trade in stored_trades:
        id_hash = generate_trade_hash(trade_api, stored_trade[11])
        if db_functions.check_trade_uid(id_hash):
            custom_logging.add_log(f"Trade {trade_api['symbol']} placed @ {trade_api['entryPrice']} is already in the database with id {id_hash}.")
            is_new = False
            profit = db_functions.check_for_profit(stored_trade)
            if profit:
                profit_message = ProfitTradeMessage(stored_trade[1], profit, stored_trade[7])
                message_text = profit_message.generate_message()
                send_telegram_message(CALLS_CHANNEL_ID, message_text, reply_to_message_id=stored_trade[9])
                custom_logging.add_log(f"Trade {stored_trade[1]} has reached a profit of {profit}%")
            break

    if trade_api["updateTimeStamp"] < (int(time() * 1000) - 150000):
        custom_logging.add_log(f"Trade {trade_api['symbol']} placed @ {trade_api['entryPrice']} is older than 2.5 minutes.")
        is_new = False
    if percentage_difference > 3:
        custom_logging.add_log(f"Trade {trade_api['symbol']} placed @ {trade_api['entryPrice']} is more than 3% away from current price ({percentage_difference}).")
        is_new = False 
 
    return is_new


def is_trade_closed(api_trades, stored_trade):
    """
    Check if a trade is closed.

    :param api_trades: A list of trades from the API.
    :param stored_trade: A stored trade to check against the API trades.
    :return: True if the trade is closed, False otherwise.
    """
    is_closed = True
    if api_trades:    
        for api_trade in api_trades:
            id_hash = generate_trade_hash(api_trade, stored_trade[11])

            if id_hash == stored_trade[0]:
                is_closed = False
                db_functions.update_trade(api_trade, stored_trade[0],stored_trade[13])
                break

    return is_closed
