import logging
import pandas as pd
from src.telegram_api_handler import TelegramApi
from time import gmtime

# logging basic config
FORMAT = '%(asctime)s--%(levelname)s--%(message)s'
logging.basicConfig(filename='Bot_logs.log', filemode='a', format=FORMAT, level=logging.INFO)


class Main:
    def __init__(self):
        telegram = TelegramApi()
        update_id = None
        tarea_checker = False

        while True:
            updates = telegram.get_updates(offset=update_id)
            updates = updates["result"]
            if len(updates) != 0:
                logging.info(updates)
            if updates:
                # print(updates)
                for item in updates:
                    update_id = item["update_id"]
                    try:
                        if item.has("message"):
                            cuerpo = item["message"]
                            chat_id = cuerpo["chat"]["id"]
                            tarea = "texto"
                            msg_id = chat_id
                        elif item.has("callback_query"):
                            cuerpo = item["callback_query"]["message"]
                            chat_id = cuerpo["chat"]["id"]
                            msg_id = item["callback_query"]["message"]["message_id"]
                            tarea = item["callback_query"]["data"]
                            tarea_checker = True
                        else:       # solucion temporal
                            print(item)
                            cuerpo = item
                            chat_id = None
                            tarea = "texto"
                            msg_id = chat_id
                    except:
                        # cuerpo = item["edited_message"]
                        cuerpo = item["callback_query"]["message"]
                        chat_id = cuerpo["chat"]["id"]
                        msg_id = item["callback_query"]["message"]["message_id"]
                        tarea = item["callback_query"]["data"]
                        tarea_checker = True
                        # aqui ya tenemos la tarea que queremos

                    try:
                        # Comandos telegram
                        try:
                            entities = cuerpo['entities']
                        except:
                            entities = []
                        for element in entities:
                            # Protocolo de insercion en un grupo
                            if str(element["type"]) == "bot_command":
                                logging.info("bot command detected")

                    except KeyError:
                        logging.exception("Error traceback")
                    try:
                        if item and "photo" not in cuerpo and "voice" not in cuerpo and \
                                "document" not in cuerpo and "video" not in cuerpo:
                            try:
                                menu_handler(telegram, cuerpo, chat_id, msg_id, tarea_checker, tarea)

                            except:
                                logging.exception("Error traceback")
                                try:
                                    if cuerpo["new_chat_member"]["username"] == "TheRoomFatherBot":
                                        logging.info('%s', "--------------------NEW CLIENT--------------------")
                                        telegram.send_message("Hola, encantado de conocerle", cuerpo["chat"]["id"])
                                        telegram.send_initial_menu(cuerpo["chat"]["id"])
                                except KeyError:
                                    logging.exception("Error traceback")

                        elif "document" in cuerpo:

                            logging.info("document detected, but not sure what to do with it")
                        else:
                            telegram.send_message("lo siento, no entiendo prueba otra vez", chat_id)
                            logging.warning("not sure what to do with this message")
                    except:
                        logging.exception("Error traceback")

    def menu_handler(self, tarea_checker, tarea):
        if not tarea_checker:
            telegram.send_initial_menu(chat_id)
        else:
            telegram.edit_message(msg_id, chat_id, tarea)
            if tarea.isdigit():
                tarea_checker = False
                telegram.send_initial_menu(chat_id)
        try:
            if cuerpo["text"]:
                message = cuerpo["text"].lower()
            else:
                message = "un mensaje que no se que es"
        except:
            print(cuerpo)

        if "text" in cuerpo and cuerpo["text"].lower() == "/adios":
            tarea_checker = False
            print()  # reiniciariamos el bot para otra ocasion
            telegram.send_menu(chat_id)

        return message


if __name__ == "__main__":
    Main()
