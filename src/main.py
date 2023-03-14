
import sql_functions
import binance
import trades as trades_functions
import bot_actions as bot



top10 =  binance.get_top_traders(10)

for trader_id,trader_name in top10:
     #sql_functions.insert_trader(trader_id,trader_name)     
     trades = binance.get_trader_trades(trader_id)
     stored_trades = sql_functions.get_trades(trader_id)
     for trade in trades:
          if(trades_functions.check_for_new_trade(stored_trades,trade)):
               msg_id = bot.send_message_to_channel("Nouveau trade détécté 🚨 \nTrader: {} \nPaire: {} \nTrade: {} \n Prix d'achat: {}".format(trader_name,trade['symbol'],"Long 🟢" if trade['amount'] > 0 else "Short 🔴",trade['entryPrice']))
               sql_functions.insert_trade(trade,trader_id,msg_id)
     for s_trade in stored_trades:
          if(trades_functions.check_for_closed_trade(trades,s_trade)):
               bot.send_message_to_channel("""
               Trade cloturé 🚨 \n
               Trader: {} \n
               Paire: {} \n
               Trade: {} \n
               Profit: {}% \n
               Prix de fermeture: {}
               """.format(trader_name,s_trade['symbol'],"Long 🟢" if s_trade['amount'] > 0 else "Short 🔴",float(s_trade['roe'])*100 ,s_trade['mark_price']))