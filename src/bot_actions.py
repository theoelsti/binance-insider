import requests
from time import sleep
import errors_printing as errors
BOT_API_KEY = '6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM'
CHANNEL_NAME = '-1001835398982'

def send_message_to_channel(message_text):
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CHANNEL_NAME,
        'text': message_text
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        errors.print_error("Error during message sending : "+response.text)
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        send_message_to_channel(message_text)

def send_open_trade_message_to_channel(trade,trader_name):
    message_text = "🚨 New trade  \n📩Pair: {} \n{}\n💯Leverage: Cross {}x \n\n📊Entry: {}\n🧑Trader: {}".format(
                        trade["symbol"],
                        "📈Direction: Long" if trade["amount"] > 0 else "📉Direction: Short",
                        trade["leverage"],
                        trade["entryPrice"],
                        trader_name
                    )

    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CHANNEL_NAME,
        'text': message_text
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print("Error during message sending : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        send_open_trade_message_to_channel(trade,trader_name)

def reply_message_to_channel(message_text,message_id):
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CHANNEL_NAME,
        'reply_to_message_id': message_id,
        'text': message_text
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print("Error during message reply : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        reply_message_to_channel(message_text,message_id)

def reply_closed_trade_to_channel(s_trade,trader_name):
    message_text =  """⚠️Closed trade\n\n📩Pair: {} \n✅Profit: {}% \nClosing Price: {}""".format(
                        s_trade[1],
                        round(float(s_trade[5])*100, 2),
                        s_trade[3]
                    )
    
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CHANNEL_NAME,
        'reply_to_message_id': s_trade[9],
        'text': message_text
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print("Error during message reply : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        reply_closed_trade_to_channel(s_trade,trader_name)
