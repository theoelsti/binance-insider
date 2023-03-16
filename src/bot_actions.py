import requests
from time import sleep,time
import errors_printing as errors
from misc_functions import format_timestamp
BOT_API_KEY         = '6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM'
CALLS_CHANNEL_NAME  = '-1001835398982'
PUBLIC_CHANNEL_NAME = '-1001864787410'

def send_message_to_channel(message_text):
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CALLS_CHANNEL_NAME,
        'text': message_text,
        'protect_content': True
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        errors.print_error("Error during message sending : "+response.text)
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        send_message_to_channel(message_text)

def send_open_trade_message_to_channel(trade,trader_name):
    message_text = "📩Pair: {} \n{}\n💯Leverage: Cross {}x \n\n📊Entry: {}\n🧑Trader: {}".format(
                        trade["symbol"],
                        "📈Direction: Long" if trade["amount"] > 0 else "📉Direction: Short",
                        trade["leverage"],
                        trade["entryPrice"],
                        trader_name
                    )

    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CALLS_CHANNEL_NAME,
        'text': message_text,
        'protect_content': True
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
        'chat_id': CALLS_CHANNEL_NAME,
        'reply_to_message_id': message_id,
        'text': message_text,
        'protect_content': True,
        'allow_sending_without_reply': True
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print("Error during message reply : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        reply_message_to_channel(message_text,message_id)

def reply_closed_trade_to_channel(s_trade,trader_name):
    message_text =  """⚠️Close trade\n✅Profit: {}%\n⌛️Time: {}""".format(
                        round(float(s_trade[5])*100, 2),
                        format_timestamp(time()-s_trade[7])
                    )
    
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CALLS_CHANNEL_NAME,
        'reply_to_message_id': s_trade[9],
        'text': message_text,
        'disable_notification': True,
        'protect_content': True,
        'allow_sending_without_reply': True
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print("Error during message reply : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        reply_closed_trade_to_channel(s_trade,trader_name)

def reply_profit_trade_to_channel(pair,profit,timestamp,message_id):
    message_text =  """✅Profit: {}%\n⌛️Time: {}""".format(
                        profit,
                        format_timestamp(time()-timestamp)
                    )
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': CALLS_CHANNEL_NAME,
        'reply_to_message_id': message_id,
        'text': message_text,
        'disable_notification': True,
        'protect_content': True
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print("Error during message reply : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        reply_profit_trade_to_channel(pair,profit,timestamp,message_id)

def send_message_to_public_channel(message_text):
    sent_message = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': PUBLIC_CHANNEL_NAME,
        'text': message_text,
        'parse_mode': 'Markdown',
        'disable_web_page_preview ': 1
    })
    if sent_message.status_code == 200:
        return sent_message.json()['result']['message_id']
    else:
        print("Error during message sending : "+sent_message.text)
