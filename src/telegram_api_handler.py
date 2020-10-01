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

    def send_message(self, msg, chat_id, keyBoard=None):
        if keyBoard:
            url = self.base + f"sendMessage?chat_id={chat_id}&text={msg}&reply_markup={keyBoard}"
        else:
            url = self.base + f"sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)

    def edit_message(self, msg_id, chat_id, texto, keyBoard=None):
        if keyBoard:
            url = self.base + f"editMessageText?chat_id={chat_id}&message_id={msg_id}&text={texto}&reply_markup={keyBoard}"
        else:
            url = self.base + f"editMessageText?chat_id={chat_id}&message_id={msg_id}&text={texto}"
        try:
            # print(requests.get(url).content)  # para testing
            requests.get(url)
        except:
            logging.exception("Error traceback")

    def delete_message(self, chat_id, msg_id):
        url = self.base + f"deleteMessage?chat_id={chat_id}&message_id={msg_id}"
        r = requests.get(url)
        response = json.loads(r.content)
        if not response["ok"]:
            print(response)
