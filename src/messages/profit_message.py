from trades.trades_functions import generate_table_trades
from api.telegram import send_telegram_message
from database.db_functions import get_sum_profit,delete_daily_trades,insert_daily_profit,get_count_winning_loosing_trades
from datetime import datetime
from config import PUBLIC_CHANNEL_NAME as public_channel

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
        message += f"Total Profit: _{round(self.profit*100,3)}%_ 💰\n"
        message += f"Total Losses: _{round(self.losses*100,3)}%_ 😢\n"
        message += f"Net Profit: *{round((self.profit + self.losses)*100,3)}%* 🚀\n"


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
    send_telegram_message(public_channel,message,protect_content=False,parse_mode="Markdown")

    daily_count = get_count_winning_loosing_trades()
    insert_daily_profit(daily_count[0][0],daily_count[1][0],total_profit)

    delete_daily_trades()

message = """
🚀 **18-03-2023 - Daily Profit Announcement!** 🚀

Hey everyone! We've had another fantastic trading day! Here's a quick summary of our top trades:

🥇 *Top 3 Winning Trades:*
[Trade n°1](https://t.me/c/1835398982/1586) : #BTCUSDT - Profit: _272.9%_ 💰
[Trade n°2](https://t.me/c/1835398982/2030) : #BNBUSDT - Profit: _157.1%_ 💰
[Trade n°3](https://t.me/c/1835398982/1811) : #ATOMUSDT - Profit: _22.6%_ 💰

🛑 *Top 3 Losing Trades:*
[Trade n°1](https://t.me/c/1835398982/1984) : #ETHUSDT - Loss: _-236.0%_ 😢
[Trade n°2](https://t.me/c/1835398982/909) : #BTCUSDT - Loss: _-131.9%_ 😢
[Trade n°3](https://t.me/c/1835398982/1812) : #BTCUSDT - Loss: _-59.7%_ 😢

📈 *Overall Performance:*
Total Profit: _675.064%_ 💰
Total Losses: _-525.117%_ 😢
Net Profit: *149.947%* 🚀

We're proud of our overall performance and excited to keep bringing you the best trading signals! Let's keep up the momentum 🚀 

Remember to manage your risks and follow our trading guidelines.

To join us and get access to our exclusive trading signals, just contact our [bot](https://t.me/BinanceInsider_bot) or visit our [online shop](https://binanceinsider.mysellix.io) and order your ticket!

Sign up on [MEXC](https://www.mexc.com/register?inviteCode=1auka), our recommended exchange, and enjoy the lowest trading fees in the market! 💰
"""
send_telegram_message(public_channel,message,protect_content=False,parse_mode="Markdown")
