import sql_functions
import bot_actions as bot
import trades as trades_functions

def check_opened_trades(trades, stored_trades,trader_name):
     for s_trade in stored_trades:
          if trades_functions.check_for_closed_trade(trades, s_trade):
               sql_functions.delete_trade(s_trade[0])
               bot.reply_closed_trade_to_channel(s_trade, trader_name)

def check_closed_trades(trades, stored_trades,trader_name,trader_id):
     for trade in trades:
          if trades_functions.check_for_new_trade(stored_trades, trade):
            msg_id = bot.send_open_trade_message_to_channel(trade, trader_name)
            sql_functions.insert_trade(trade, trader_id, msg_id)
          else:
               
