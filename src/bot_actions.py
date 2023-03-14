import requests
from time import sleep
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
        print("Error during message sending : "+response.text)  # Do what you want with response
        print("Retry after "+str(response.json()['parameters']['retry_after'])+" seconds")
        sleep(response.json()['parameters']['retry_after'])
        send_message_to_channel(message_text)

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
