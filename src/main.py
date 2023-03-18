
import database.db_functions as db_functions
import api.binance_api as binance_api
import trades.trades as trades_functions
import api.telegram as bot
from time import sleep, time
import trades.trades_functions as checks
import datetime
from messages.profit_message import send_daily_message
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
          script_startup = datetime.datetime.now()
          while working:
               closed_trades = get_closed_trade()
               if script_startup.hour >= 21 and script_startup.minute < 15 and closed_trades != []:
                   print("Time to close")
                   send_daily_message()
                   working = False
                   break
               current_time = time()
               if current_time - last_print_time >= 60:
                    last_print_time = current_time
                    print("[i] Bot is running. Total trades stored : " + str(db_functions.count_total_trades()))
               main()
               sleep(15)
          print("Exiting")
     except KeyboardInterrupt:
          print("Exiting")