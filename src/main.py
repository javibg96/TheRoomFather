import logging
import pandas as pd
from src.telegram_api_handler import TelegramApi
from src.updates_handler import updater
from src.menu_handler import menu_handler
from time import gmtime

# logging basic config
FORMAT = '%(asctime)s--%(levelname)s--%(message)s'
logging.basicConfig(filename='Bot_logs.log', filemode='a', format=FORMAT, level=logging.INFO)


class Main:
    def __init__(self):
        logging.info("STARTING BOT......")
        telegram = TelegramApi()
        user = [None, None, None, None]
        updater_values = [None, None, None, 0, 0, "texto", user]
        # [update_id, item, cuerpo, chat_id, msg_id, tarea, user]

        while True:
            try:
                tarea_ant = updater_values[5]
                updater_values = updater(telegram, updater_values)

                [item, cuerpo, chat_id, msg_id, tarea, user] = updater_values[1:7]
            except KeyError:
                logging.exception("Error traceback")
                raise
            if item and tarea_ant != tarea:
                try:
                    elementos = ["photo", "voice", "document", "video"]
                    if all([elemento not in cuerpo for elemento in elementos]):
                        try:
                            menu_handler(cuerpo, chat_id, msg_id, tarea, user)
                        except:
                            logging.exception("Error traceback")
                    elif "document" in cuerpo:
                        telegram.send_message("lo siento, no entiendo, prueba otra vez", chat_id)
                        logging.info("document detected, but not sure what to do with it")
                    else:
                        telegram.send_message("lo siento, no entiendo, prueba otra vez", chat_id)
                        logging.warning("not sure what to do with this message")
                except:
                    logging.exception("Error traceback")


if __name__ == "__main__":
    Main()
