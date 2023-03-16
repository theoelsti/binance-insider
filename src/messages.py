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

        message += "🥇 **Top 3 Winning Trades:**\n"
        for i, trade in enumerate(self.winning_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/{CALLS_CHANNEL_NAME}/{trade['message_id']}) : #{trade['pair']} - Profit: *{trade['profit']}%* 💰\n"

        message += "\n🛑 **Top 3 Losing Trades:**\n"
        for i, trade in enumerate(self.losing_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/{CALLS_CHANNEL_NAME}/{trade['message_id']}) : #{trade['pair']} - Loss: *{abs(trade['profit'])}%* 😢\n"

        message += "\nWe're proud of our overall performance and excited to keep bringing you the best trading signals! Let's keep up the momentum! 🚀\n"

        message += "Remember to manage your risks and follow our trading guidelines. If you have any questions, feel free to reach out to our support team. Happy trading! 🎉"

        return message

# Example usage

trades = generate_table_trades()
winning_trades = trades[0]
losing_trades = trades[1]

profit_message = ProfitMessage(winning_trades, losing_trades)
message = profit_message.generate_message()
send_message_to_public_channel(message)
