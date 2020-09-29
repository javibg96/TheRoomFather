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

    def edit_message(self, msg_id, chat_id, option):
        if option == "limpieza":
            pregunta = "¿Que cantidad de horas necesita?"
            keyBoard = '{"inline_keyboard": [[{"text": "2 horas", "callback_data": 2}], [{"text": "4 horas", ' \
                       '"callback_data": 4}], [{"text": "6 horas", "callback_data": 6}]]} '
            url = self.base + f"editMessageText?chat_id={chat_id}&message_id={msg_id}&text={pregunta}&reply_markup={keyBoard}"
        elif option.isdigit():      # horas de limpieza
            texto = f"Perfecto, ahora mismo enviamos a un equipo para que limpie {option} horas, buen dia"
            url = self.base + f"editMessageText?chat_id={chat_id}&message_id={msg_id}&text={texto}"
        else:
            texto = "escriba en que puedo ayudarle a ver si puedo encontrar alguna solución"
            url = self.base + f"editMessageText?chat_id={chat_id}&message_id={msg_id}&text={texto}"
        try:
            print(requests.get(url).content)
        except:
            logging.exception("Error traceback")

    def send_initial_menu(self, chat_id):
        pregunta = "Bienvenido, ¿Qué quieres hacer?"
        keyBoard = '{"inline_keyboard": [[{"text": "Limpieza", "callback_data": "limpieza"}], [{"text": "otro", ' \
                   '"callback_data": "otro"}]]} '
        url = self.base + f"sendMessage?chat_id={chat_id}&text={pregunta}&reply_markup={keyBoard}"
        try:
            print(requests.get(url).content)
        except:
            logging.exception("Error traceback")
