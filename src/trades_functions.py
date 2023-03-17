import sql_functions
import bot_actions as bot
import trades as trades_functions
from math import trunc
def check_closed_trades(trades, stored_trades,trader_name):
     for s_trade in stored_trades:
          if trades_functions.check_for_closed_trade(trades, s_trade):
               sql_functions.delete_trade(s_trade)
               bot.reply_closed_trade_to_channel(s_trade, trader_name)

def check_opened_trades(trades, stored_trades,trader_name,trader_id):
     for trade in trades:
          if trades_functions.check_for_new_trade(stored_trades, trade):
            msg_id = bot.send_open_trade_message_to_channel(trade, trader_name)
            sql_functions.insert_trade(trade, trader_id, msg_id)

def generate_table_trades():
     trades = sql_functions.get_winning_losing_trades()
     # Format : trade_id, symbol, opened, closed, message_id, profit

     # Generate two {} arrays, named winning_trades and losing_trades, with indexes : message_id, symbol, opened, closed, profit
     winning_trades = []
     losing_trades = []

     for trade in trades[0]:
          winning_trades.append({'message_id': trade[4], 'pair': trade[1], 'opened': trade[2], 'closed': trade[3], 'profit': round(trade[5],3)})
     for trade in trades[1]:
          losing_trades.append({'message_id': trade[4], 'pair': trade[1], 'opened': trade[2], 'closed': trade[3], 'profit': round(trade[5],3)})

     return([winning_trades, losing_trades])