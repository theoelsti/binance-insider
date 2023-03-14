
import sql_functions
import binance
import trades as trades_functions
import bot_actions as bot
from time import sleep
from bot_user_app import init_app
def main():
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
                sql_functions.delete_trade(s_trade[0])
                bot.reply_message_to_channel("""Trade cloturé ✅ \nTrader: {} \nPaire: {} \nTrade: {} \nProfit: {}% \nPrix de fermeture: {}""".format(trader_name,s_trade[1],"Long 🟢" if s_trade[6] > 0 else "Short 🔴",round(float(s_trade[5]),2)*100 ,s_trade[3]),s_trade[9])

if __name__ == "__main__":
     try:
          while True:
               init_app()
               main()
               sleep(20)
     except KeyboardInterrupt:
          print("Exiting")
