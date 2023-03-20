import database.db_functions as db_functions
import api.telegram as bot
import trades.trades as trades_functions
from messages.new_trade_message import NewTradeMessage
from messages.closed_trade_message import ClosedTradeMessage
from config import CALLS_CHANNEL_NAME


def check_closed_trades(trades, stored_trades, trader_name):
    for s_trade in stored_trades:
        if trades_functions.is_trade_closed(trades, s_trade):
            db_functions.delete_trade(s_trade)
            closed_trade_message = ClosedTradeMessage(s_trade, trader_name)
            message_text = closed_trade_message.generate_message()
            bot.send_telegram_message(
                chat_id=CALLS_CHANNEL_NAME,
                message_text=message_text,
                reply_to_message_id=s_trade[9],
                disable_notification=True
            )
def check_opened_trades(trades, stored_trades, trader_name, trader_id):
    for trade in trades:
        if trades_functions.is_trade_new(stored_trades, trade):
            new_trade_message = NewTradeMessage(trade, trader_name)
            message_text = new_trade_message.generate_message()
            msg_id = bot.send_telegram_message(CALLS_CHANNEL_NAME,message_text)
            db_functions.insert_trade(trade, trader_id, msg_id)

def generate_table_trades():
     
     trades = db_functions.get_winning_losing_trades()
     winning_trades = []
     losing_trades = []

     for trade in trades[0]:
          winning_trades.append({'message_id': trade[4], 'pair': trade[1], 'opened': trade[2], 'closed': trade[3], 'profit': round(trade[5],3)})
     for trade in trades[1]:
          losing_trades.append({'message_id': trade[4], 'pair': trade[1], 'opened': trade[2], 'closed': trade[3], 'profit': round(trade[5],3)})

     return([winning_trades, losing_trades])

def generate_opened_trade_table():
     trades = db_functions.get_opened_trades()
     opened_trades = []
     for trade in trades:
          opened_trades.append({'message_id': trade[8], 'pair': trade[1], 'opened': trade[6], 'profit': round(trade[5],3)})
     return(opened_trades)