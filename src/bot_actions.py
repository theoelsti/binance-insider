
import requests

BOT_API_KEY = '6089060960:AAEqhHfUVLgfnS0QsbEA4pcRl_jQ1STDQJM'
MY_CHANNEL_NAME = '-1001835398982'

def send_message_to_channel(message_text):
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': MY_CHANNEL_NAME,
        'text': message_text
    })
    if response.status_code == 200:
        return response.json()['result']['message_id']
    else:
        print(response.text)  # Do what you want with response
