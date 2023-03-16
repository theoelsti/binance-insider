
import sql_functions
import binance
import trades as trades_functions
import bot_actions as bot
from time import sleep, time
from bot_user_app import init_app
import trades_functions as checks
import datetime
from messages import send_daily_message
from sql_functions import get_closed_trade
top10 = []
def main():
    for trader_id, trader_name in top10:
     trades = binance.get_trader_trades(trader_id)
     stored_trades = sql_functions.get_trades(trader_id) 
     checks.check_opened_trades(trades, stored_trades, trader_name)
     checks.check_closed_trades(trades, stored_trades, trader_name,trader_id)

if __name__ == "__main__":
     try:
          app = init_app()
          top10 =  binance.get_top_traders(10)
          for trader_id,trader_name in top10:
               sql_functions.insert_trader(trader_id,trader_name)
          last_print_time = time()
          script_startup = datetime.datetime.now()
          while True:
               closed_trades = get_closed_trade()
               print(closed_trades)
               if script_startup.hour >= 21 and closed_trades != []:
                   print("C'est l'heure de la fermeture")
                   send_daily_message()

                   break
               current_time = time()
               if current_time - last_print_time >= 60:
                    last_print_time = current_time
                    print("[i] Bot is running. Total trades stored : " + str(sql_functions.count_total_trades()))
               main()
               sleep(26)
     except KeyboardInterrupt:
          print("Exiting")