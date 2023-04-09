
import database.db_functions as db_functions
import api.binance_api as binance_api
from time import sleep, time
import trades.trades_functions as checks
import datetime
from messages.profit_message import send_message
from database.db_functions import get_closed_trade,get_traders
top10 = []

def main():
    for trader_id, trader_name in top10:
     trades = binance_api.fetch_trader_trades(trader_id)
     stored_trades = db_functions.get_trades(trader_id) 
     checks.check_opened_trades(trades, stored_trades, trader_name,trader_id)
     checks.check_closed_trades(trades, stored_trades, trader_name)


if __name__ == "__main__":
     try:
          working = True
          top10 =  get_traders()
          last_print_time = time()
          current_date = datetime.datetime.now()

          print(f"[{current_date.strftime('%d-%m-%Y %H:%M:%S')}] [i] Bot is running. Total trades stored : " + str(db_functions.count_total_trades()))

          while working is True:
               current_date = datetime.datetime.now()
               closed_trades = get_closed_trade()
               if current_date.hour == 19 and current_date.minute == 00 and working is True:
                   print("Time to close")
                   send_message()
                   working = False
                   break
               current_time = time()
               if current_time - last_print_time >= 1800 and working is True:
                    last_print_time = current_time
                    # Format [DD-MM-YYYY HH:MM:SS]
                    print(f"[{current_date.strftime('%d-%m-%Y %H:%M:%S')}] [i] Bot is running. Total trades stored : " + str(db_functions.count_total_trades()))
               if working is True:
                   main()
                   sleep(20)

     except KeyboardInterrupt:
          print("Exiting")