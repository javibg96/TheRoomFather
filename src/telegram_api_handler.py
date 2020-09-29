import configparser as cfg
import json
import requests
import logging


class TelegramApi:
    def __init__(self):
        config_path = "../src/config.cfg"
        self.token = self.read_token_from_config_file(config_path)
        self.base = f"https://api.telegram.org/bot{self.token}/"
        self.base_file = f"https://api.telegram.org/file/bot{self.token}/"

    @staticmethod
    def read_token_from_config_file(config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'telegram_token')

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + f"&offset={offset + 1}"
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + f"sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)

    def send_menu(self, chat_id):
        pregunta = "Bienvenido, ¿Qué quieres hacer?"
        keyBoard = '{"inline_keyboard": [[{"text": "Limpieza", "callback_data": "limpieza"}], [{"text": "otro", ' \
                   '"callback_data": "otro"}]]} '
        url = self.base + f"sendMessage?chat_id={chat_id}&text={pregunta}&reply_markup={keyBoard}"
        try:
            print(requests.get(url).content)
        except:
            logging.exception("Error traceback")
