class NewTradeMessage:
    def __init__(self, trade, trader_name):
        self.trade = trade
        self.trader_name = trader_name

    def generate_message(self):
        direction = "📈Direction: Long" if self.trade["amount"] > 0 else "📉Direction: Short"
        message = (
            f"📩Pair: {self.trade['symbol']} \n{direction}\n"
            f"💯Leverage: Cross {self.trade['leverage']}x \n\n"
            f"📊Entry: {self.trade['entryPrice']}\n🧑Trader: {self.trader_name}"
        )
        return message