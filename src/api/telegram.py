import requests
from time import sleep
from config import BOT_API_KEY

def handle_telegram_response(response):
    if response.status_code == 200:
        return None
    else:
        print("Error during message sending : " + response.text)
        if 'retry_after' in response.json()['parameters']:
            retry_after = response.json()['parameters']['retry_after']
            print(f"Retry after {retry_after} seconds")
            return retry_after
        else:
            raise Exception("Unhandled Telegram error")

def send_telegram_message(chat_id, message_text, reply_to_message_id=None, disable_notification=False, parse_mode=None,protect_content=True):
    params = {
        'chat_id': chat_id,
        'text': message_text,
        'protect_content': protect_content,
        'disable_notification': disable_notification
    }

    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
        params['allow_sending_without_reply'] = True

    if parse_mode:
        params['parse_mode'] = parse_mode

    while True:
        response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', params)
        retry_after = handle_telegram_response(response)

        if retry_after is None:
            return response.json()['result']['message_id']
        else:
            sleep(retry_after)

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