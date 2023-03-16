from trades_functions import generate_table_trades
from bot_actions import send_message_to_public_channel
from sql_functions import get_sum_profit,delete_daily_trades,insert_daily_profit,get_count_winning_loosing_trades
from datetime import datetime


PUBLIC_CHANNEL_NAME = '1864787410'
CALLS_CHANNEL_NAME  = '1835398982'
class ProfitMessage:
    def __init__(self, winning_trades, losing_trades, profit, losses):
        self.winning_trades = winning_trades
        self.losing_trades = losing_trades
        self.profit = profit
        self.losses = losses

    def generate_message(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%d-%m-%Y')
        message = f"🚀 **{formatted_date} - Daily Profit Announcement!** 🚀\n\n"
        message += "Hey everyone! We've had another fantastic trading day! Here's a quick summary of our top trades:\n\n"
        message += "🥇 *Top 3 Winning Trades:*\n"
        for i, trade in enumerate(self.winning_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/{CALLS_CHANNEL_NAME}/{trade['message_id']}) : #{trade['pair']} - Profit: _{round(trade['profit']*100,2)}%_ 💰\n"
        message += "\n🛑 *Top 3 Losing Trades:*\n"
        for i, trade in enumerate(self.losing_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/{CALLS_CHANNEL_NAME}/{trade['message_id']}) : #{trade['pair']} - Loss: _{round(trade['profit']*100,2)}%_ 😢\n"
        message += "\n📈 *Overall Performance:*\n"
        message += f"Total Profit: _{round(self.profit,3)*100}%_ 💰\n"
        message += f"Total Losses: _{round(self.losses,3)*100}%_ 😢\n"
        message += f"Net Profit: *{round(self.profit + self.losses,3)*100}%* 🚀\n"


        message += "\nWe're proud of our overall performance and excited to keep bringing you the best trading signals! Let's keep up the momentum 🚀 \n"

        message += "\nRemember to manage your risks and follow our trading guidelines."

        message += "\n\nTo join us and get access to our exclusive trading signals, just contact our [bot](https://t.me/BinanceInsider_bot) or visit our [online shop](https://binanceinsider.mysellix.io) and order your ticket!"
        message += "\n\nSign up on [MEXC](https://www.mexc.com/register?inviteCode=1auka), our recommended exchange, and enjoy the lowest trading fees in the market! 💰"
        return message



def send_daily_message():
    trades = generate_table_trades()
    winning_trades = trades[0]
    losing_trades = trades[1]

    sum_profit = get_sum_profit()
    profit = sum_profit[0]
    losses = sum_profit[1]
    
    total_profit = profit + losses
    profit_message = ProfitMessage(winning_trades, losing_trades, profit, losses)
    message = profit_message.generate_message()
    send_message_to_public_channel(message)

    daily_count = get_count_winning_loosing_trades()
    insert_daily_profit(daily_count[0][0],daily_count[1][0],total_profit)

    delete_daily_trades()
