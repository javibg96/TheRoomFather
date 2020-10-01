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
        inicio = False
        user = [None, None, None, None]
        updater_values = [None, False, None, None, 0, 0, "texto", user]
        # [update_id, update_flag, item, cuerpo, chat_id, msg_id, tarea, user]

        while True:
            try:
                tarea_ant = updater_values[6]
                updater_values = updater(telegram, updater_values)

                [item, cuerpo, chat_id, msg_id, tarea, user] = updater_values[2:8]
                print(f"USER POST UPDATES{user}")
                if tarea in ["inicio", "cliente_registrado"]:
                    inicio = True
            except KeyError:
                logging.exception("Error traceback")
                raise
            print(f"tarea anterior: {tarea_ant},  tarea actual:{tarea}")

            if item and inicio and updater_values[1]:
                if tarea_ant != tarea:
                    try:
                        elementos = ["photo", "voice", "document", "video"]
                        if all([elemento not in cuerpo for elemento in elementos]):
                            try:
                                menu_handler(chat_id, msg_id, tarea, user)
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
            else:
                telegram.send_message("Lo siento, no puedo interaccionar con mensajes hasta la introduccion del "
                                      "comando /start", chat_id)


if __name__ == "__main__":
    Main()
