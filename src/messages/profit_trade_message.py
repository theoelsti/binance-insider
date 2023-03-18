from utils.timestamp_utils import format_timestamp
from time import time

class ProfitTradeMessage:
    def __init__(self, pair, profit, timestamp):
        self.pair = pair
        self.profit = profit
        self.timestamp = timestamp

    def generate_message(self):
        message_text = f"✅Profit: {self.profit}%\n⌛️Time: {format_timestamp(time() - self.timestamp)}"
        return message_text
