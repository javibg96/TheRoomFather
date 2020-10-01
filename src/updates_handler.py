import logging
from src.DB.DB_handler import get_client_info,check_password,check_room_availability


def updater(telegram, updater_values):
    [update_id, update_flag, item, cuerpo, chat_id, msg_id, tarea, usuario] = updater_values
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
                    [chat_id, msg_id, tarea, usuario] = cuerpo_handler(cuerpo, usuario, tarea)

                elif "callback_query" in item:
                    cuerpo = item["callback_query"]
                    [chat_id, msg_id, tarea, usuario] = cuerpo_handler(cuerpo, usuario, tarea)
                elif "edited_message" in item:
                    cuerpo = item["edited_message"]  # a partir de aqui copy paste de message
                    [chat_id, msg_id, tarea, usuario] = cuerpo_handler(cuerpo, usuario, tarea)
                else:  # solucion temporal

                    cuerpo = item
                    chat_id = None
                    tarea = "No_se"
                    msg_id = chat_id

                if "text" in cuerpo and cuerpo["text"].lower() == "/adios":
                    tarea = "texto"
                    usuario = [None, None, None, None]
                    print()  # reiniciariamos el bot para otra ocasion

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
    updater_values = [update_id, update_flag, item, cuerpo, chat_id, msg_id, tarea, usuario]
    return updater_values


def cuerpo_handler(cuerpo, usuario, tarea):

    if "message" in cuerpo:
        tarea = cuerpo["data"]
        cuerpo = cuerpo["message"]

    chat_id = cuerpo["chat"]["id"]
    msg_id = cuerpo["message_id"]

    if cuerpo["text"].lower() == "/start":
        logging.info("Wake up protocol, let's check if is someone known")
        tarea = "inicio"
        client_id = str(cuerpo["from"]["id"])
        if get_client_info(client_id):
            cliente = get_client_info(client_id)
            usuario = [client_id, cliente["nombre"], cliente["password"], cliente["piso"]]
            tarea = "cliente_registrado"
    if "animation" in cuerpo:
        telegram.delete_message(chat_id, msg_id)
        tarea = "texto"
    else:
        if tarea == "registro":
            usuario[0] = cuerpo["from"]["id"]
            user = cuerpo["text"].lower()
            usuario[1] = user  # nombre de usuario, necesaria validacion de nombre
            tarea = "password"
        elif "password" in tarea:
            password = cuerpo["text"].lower()
            if check_password(password):
                usuario[2] = password  # contraseña, necesaria validacion de long, caracteres...
                tarea = "reg_hab"
            else:
                tarea = "w_password"
        elif tarea in ["hab", "w_hab"]:
            habitacion = cuerpo["text"].lower()
            if check_room_availability(habitacion):
                usuario[3] = habitacion
                tarea = "registro_completado"
            else:
                tarea = "w_hab"
        elif tarea == "nohab":
            habitacion = None
            usuario[3] = habitacion
            tarea = "registro_completado"
        else:
            mensaje = cuerpo["text"].lower()
    return chat_id, msg_id, tarea, usuario
