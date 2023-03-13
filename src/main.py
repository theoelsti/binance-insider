
import sqlFunctions
import binance
import trades as trades_functions
import bot_actions as bot



top10 =  binance.get_top_traders(10)

for trader_id,trader_name in top10:
     sqlFunctions.insert_trader(trader_id,trader_name)
     
     trades = binance.get_trader_trades(trader_id)

     # Vérifie si le trade est déjà enregistré
     for trade in trades:
          stored_trades = sqlFunctions.get_trades(trader_id)
          if(trades_functions.check_for_new_trade(stored_trades,trade)):
               msg_id = bot.send_message_to_channel("Nouveau trade détécté 🚨 \nTrader: {} \nPaire: {} \nTrade: {} \n Prix d'achat: {}".format(trader_name,trade['symbol'],"Long 🟢" if trade['amount'] > 0 else "Short 🔴",trade['entryPrice']))
               sqlFunctions.insert_trade(trade,trader_id,msg_id)