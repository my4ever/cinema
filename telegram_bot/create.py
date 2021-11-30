import requests

from . setups import default_keyboard


class Bot:
    def __init__(self, token):
        self.url = f'https://api.telegram.org/bot{token}/'

    def send_message(self, chat_id, text='Вот что я нешел: \n', keyboard=default_keyboard):
        command = 'sendMessage'
        data = {'chat_id': chat_id,
                'text': text,
                'reply_markup': {
                    'keyboard': keyboard,
                    'resize_keyboard': True
                }
                }
        requests.post(url=self.url + command, json=data)


set_webhook = 'https://api.telegram.org/bot/setWebhook?url=https://7128-195-78-104-11.ngrok.io/bot/yougotmsg/'
