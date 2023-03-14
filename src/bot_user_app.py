from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackContext, Updater,CallbackQueryHandler

BOT_API_KEY = '6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM'

async def keyboard_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "subscribe_monthly":
        payment_protocol = "Payment protocol for monthly subscription."
    elif query.data == "subscribe_quarterly":
        payment_protocol = "Payment protocol for quarterly subscription."
    elif query.data == "subscribe_annually":
        payment_protocol = "Payment protocol for annual subscription."
    elif query.data == "subscribe_lifetime":
        payment_protocol = "Payment protocol for lifetime subscription."
    
    await query.edit_message_text(
        text=payment_protocol
    )


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("1 mois (10 $)", callback_data="subscribe_monthly"),
            InlineKeyboardButton("3 mois (25 $)", callback_data="subscribe_quarterly")
        ],
        [
            InlineKeyboardButton("1 an (90 $)", callback_data="subscribe_annually"),
            InlineKeyboardButton("A vie (250 $)", callback_data="subscribe_lifetime")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
    "Choisissez un forfait d'abonnement :",
    reply_markup=reply_markup)  


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


def init_app():   
    app = ApplicationBuilder().token(BOT_API_KEY).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CallbackQueryHandler(keyboard_callback))
    app.run_polling()