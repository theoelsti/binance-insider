import sql_functions
PUBLIC_CHANNEL_NAME = '1864787410'
class ProfitMessage:
    def __init__(self, winning_trades, losing_trades):
        self.winning_trades = winning_trades
        self.losing_trades = losing_trades

    def generate_message(self):
        message = "🚀 **Daily Profit Announcement!** 🚀\n\n"

        message += "Hey everyone! We've had another fantastic trading day! Here's a quick summary of our top trades:\n\n"

        message += "🥇 **Top 3 Winning Trades:**\n"
        for i, trade in enumerate(self.winning_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/PUBLIC_CHANNEL_NAME/{trade['message_id']}) - Profit: *{trade['profit']}%* 💰\n"

        message += "\n🛑 **Top 3 Losing Trades:**\n"
        for i, trade in enumerate(self.losing_trades, start=1):
            message += f"[Trade n°{i}](https://t.me/c/PUBLIC_CHANNEL_NAME/{trade['message_id']}) - Loss: *${abs(trade['profit'])}* 😢\n"

        message += "\nWe're proud of our overall performance and excited to keep bringing you the best trading signals! Let's keep up the momentum! 🚀\n"

        message += "Remember to manage your risks and follow our trading guidelines. If you have any questions, feel free to reach out to our support team. Happy trading! 🎉"

        return message

# Example usage:
winning_trades = [
    {"id": 1, "profit": 120},
    {"id": 2, "profit": 80},
    {"id": 3, "profit": 60},
]

losing_trades = [
    {"id": 4, "profit": -30},
    {"id": 5, "profit": -20},
    {"id": 6, "profit": -10},
]



profit_message = ProfitMessage(winning_trades, losing_trades)
message = profit_message.generate_message()
print(message)
