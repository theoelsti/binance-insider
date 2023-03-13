from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import binance
# # Build a telegram bot that is used by clients that want to purchase my private channel, and kick them after a month

# Create the command subscribe 

test_trades = binance.get_trader_trades("A6CCDBA73F3002E07F19C2D196E3CEA6")

for trade in test_trades:
     print(trade)



     
# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# app = ApplicationBuilder().token("6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()