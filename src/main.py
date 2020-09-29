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
                print(updates)
                for item in updates:
                    update_id = item["update_id"]
                    try:
                        cuerpo = item["message"]
                        chat_id = cuerpo["chat"]["id"]
                        tarea = "texto"
                    except:
                        # cuerpo = item["edited_message"]
                        cuerpo = item["callback_query"]["message"]
                        chat_id = cuerpo["chat"]["id"]
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
                                if not tarea_checker:
                                    telegram.send_menu(chat_id)
                                else:
                                    telegram.send_message(f"Tarea {tarea} recibida, nos encargaremos de ello lo antes "
                                                          f"posible", chat_id)

                                try:
                                    if cuerpo["text"]:
                                        message = cuerpo["text"].lower()

                                    else:
                                        message = "un mensaje que no se que es"
                                except:

                                    print(cuerpo)

                                if "text" in cuerpo and cuerpo["text"].lower() == "/adios":
                                    print()  # reiniciariamos el bot para otra ocasion
                                    telegram.send_menu(chat_id)
                            except:
                                logging.exception("Error traceback")
                                try:
                                    if cuerpo["new_chat_member"]["username"] == "TheRoomFatherBot":
                                        logging.info('%s', "--------------------NEW CLIENT--------------------")
                                        telegram.send_message("Hola, encantado de conocerle", cuerpo["chat"]["id"])
                                        telegram.send_menu(cuerpo["chat"]["id"])
                                except KeyError:
                                    logging.exception("Error traceback")

                        elif "document" in cuerpo:

                            logging.info("document detected, but not sure what to do with it")
                        else:
                            telegram.send_message("lo siento, no entiendo prueba otra vez", chat_id)
                            logging.warning("not sure what to do with this message")
                    except:
                        logging.exception("Error traceback")


if __name__ == "__main__":
    Main()
