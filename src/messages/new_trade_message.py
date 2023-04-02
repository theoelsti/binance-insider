class NewTradeMessage:
    def __init__(self, trade, trader_name):
        self.trade = trade
        self.trader_name = trader_name

    def generate_message(self):
        direction = "📈Direction: Long" if self.trade["amount"] > 0 else "📉Direction: Short"
        message = (
            f"📩Pair: {self.trade['symbol']} \n{direction}\n"
            f"💯Leverage: Cross {self.trade['leverage']}x \n"
            f"📊Entry: {self.trade['entryPrice']}$\n\n"
            f"👤Trader: {self.trader_name}\n"
            f"💰Stake : {abs(round((self.trade['amount']*self.trade['entryPrice'])/self.trade['leverage']))}$"
        )
        return message