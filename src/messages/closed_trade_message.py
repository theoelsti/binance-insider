from utils.timestamp_utils import format_timestamp
from time import time

class ClosedTradeMessage:
    def __init__(self, s_trade, trader_name):
        self.s_trade = s_trade
        self.trader_name = trader_name

    def generate_message(self):
        message_text = f"""
        ⚠️Close trade\n✅Profit: {round(float(self.s_trade[5]) * 100, 2)}%\n⌛️Time: {format_timestamp(time() - self.s_trade[7])}\n\n🔻Drawdown : {round(float(self.s_trade[13]) * 100, 2)}%\n
        """
        return message_text