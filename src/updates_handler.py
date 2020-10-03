import logging


def updater(telegram, updater_values, tarea_ant):
    [update_id, update_flag, cuerpo, chat_id, msg_id, tarea] = updater_values
    updates = telegram.get_updates(offset=update_id)
    updates = updates["result"]

    if len(updates) != 0:
        logging.info(updates)
        update_flag = True
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                if "message" in item:
                    cuerpo = item["message"]
                    [chat_id, msg_id, tarea_ant, tarea] = cuerpo_handler(cuerpo, tarea_ant, tarea)
                elif "callback_query" in item:
                    cuerpo = item["callback_query"]
                    [chat_id, msg_id, tarea_ant, tarea] = cuerpo_handler(cuerpo, tarea_ant, tarea)
                elif "edited_message" in item:
                    cuerpo = item["edited_message"]  # a partir de aqui copy paste de message
                    [chat_id, msg_id, tarea_ant, tarea] = cuerpo_handler(cuerpo, tarea_ant, tarea)

                else:  # solucion temporal
                    cuerpo = item
                    chat_id = None
                    tarea = "No_se"
                    msg_id = chat_id

                if "animation" in cuerpo:
                    telegram.delete_message(chat_id, msg_id)
                    tarea = "texto"
            except:
                logging.exception("error traceback")
                # cuerpo = item["edited_message"]
                print(item)
                cuerpo = item
                chat_id = None
                msg_id = chat_id

    # Comandos telegram
    try:
        entities = cuerpo['entities']
    except:
        entities = []
    for element in entities:
        # Protocolo de insercion en un grupo
        if str(element["type"]) == "bot_command":
            logging.info("bot command detected")
    updater_values = [update_id, update_flag, cuerpo, chat_id, msg_id, tarea]
    return updater_values, tarea_ant


def cuerpo_handler(cuerpo, tarea_ant, tarea="texto"):
    if "message" in cuerpo:     # esto significa que es menu no mensaje de texto
        tarea = cuerpo["data"]
        cuerpo = cuerpo["message"]

    elif tarea == "atras":
        tarea = tarea_ant
        tarea_ant = "texto"

    else:
        tareas_texto = {"registro": "usuario", "usuario": "password", "w_hab": "reg_hab", "hab": "reg_hab",
                        "w_password": "password", "texto": "texto", "inicio": "inicio", "inicio_admin": "inicio_admin",
                        "reg_piso": "add_piso", "delete_client": "deleted_client"}
        tarea = tareas_texto[tarea]

    chat_id = cuerpo["chat"]["id"]
    msg_id = cuerpo["message_id"]

    if cuerpo["text"].lower() == "/start":
        logging.info("Wake up protocol, let's check if is someone known")
        tarea = "inicio"

    return chat_id, msg_id, tarea_ant, tarea
