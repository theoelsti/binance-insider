from trades_functions import generate_table_trades
from bot_actions import send_message_to_public_channel
PUBLIC_CHANNEL_NAME = '1864787410'
CALLS_CHANNEL_NAME  = '1835398982'
class ProfitMessage:
    def __init__(self, winning_trades, losing_trades):
        self.winning_trades = winning_trades
        self.losing_trades = losing_trades

    def generate_message(self):
        message = "🚀 **Daily Profit Announcement!** 🚀\n\n"

        message += "Hey everyone! We've had another fantastic trading day! Here's a quick summary of our top trades:\n\n"

        message += "🥇 *Top 3 Winning Trades:*\n"
        for i, trade in enumerate(self.winning_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/{CALLS_CHANNEL_NAME}/{trade['message_id']}) : #{trade['pair']} - Profit: _{trade['profit']}%_ 💰\n"

        message += "\n🛑 *Top 3 Losing Trades:*\n"
        for i, trade in enumerate(self.losing_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/{CALLS_CHANNEL_NAME}/{trade['message_id']}) : #{trade['pair']} - Loss: _{abs(trade['profit'])}%_ \n"

        message += "\nWe're proud of our overall performance and excited to keep bringing you the best trading signals! Let's keep up the momentum! \n"

        message += "\nRemember to manage your risks and follow our trading guidelines."

        message += "To join us and get access to our exclusive trading signals, just [contact our bot](https://t.me/BinanceInsider_bot) or visit our [online shop](https://binanceinsider.mysellix.io) and order your ticket!\nWe're here to help you grow your crypto investment and reach new heights! 💹"
        return message

# Example usage

trades = generate_table_trades()
winning_trades = trades[0]
losing_trades = trades[1]

profit_message = ProfitMessage(winning_trades, losing_trades)
message = profit_message.generate_message()
send_message_to_public_channel(message)
