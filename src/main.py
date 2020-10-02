import logging
import pandas as pd
from src.telegram_api_handler import TelegramApi
from src.updates_handler import updater
from src.core import procesamiento_info
from src.DB.DB_handler import get_client_info, check_password, check_room_availability
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
        tarea = "texto"
        client_flag = False
        updater_values = [None, False, None, 0, 0, tarea]
        # [update_id, update_flag, cuerpo, chat_id, msg_id, tarea]

        while True:

            try:
                tarea_ant = updater_values[5]
                [updater_values, tarea_ant] = updater(telegram, updater_values, tarea_ant)
                [cuerpo, chat_id, msg_id, tarea] = updater_values[2:6]
                if tarea in ["inicio", "cliente_registrado"]:
                    inicio = True
            except KeyError:
                logging.exception("Error traceback")
                raise

            print(f"tarea anterior: {tarea_ant},  tarea actual: {tarea}")

            if cuerpo and inicio and updater_values[1]:
                if tarea_ant != tarea:
                    try:
                        elementos = ["photo", "voice", "document", "video"]
                        if all([elemento not in cuerpo for elemento in elementos]):
                            try:
                                client_id = str(cuerpo["from"]["id"])
                                if not client_flag:
                                    if get_client_info(client_id):
                                        [user, tarea] = get_client_info(client_id)
                                        client_flag = True
                                if "password" in tarea:
                                    if check_password(cuerpo["text"]):
                                        tarea = "g_password"
                                    else:
                                        tarea = "w_password"
                                elif tarea == "reg_hab":
                                    if check_room_availability(cuerpo["text"]):
                                        tarea = "g_hab"
                                    else:
                                        tarea = "w_hab"
                                # esta funcion no devuelve nada, es solo para enviar los mensajes
                                menu_handler(chat_id, msg_id, tarea, user)
                                [user, updater_values[5]] = procesamiento_info(cuerpo, tarea, user)
                                # print(f"tarea procesada:{updater_values[5]}")
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
