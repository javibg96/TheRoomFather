import logging
from src.DB.DB_handler import check_name_availability, get_client_info


def updater(telegram, updater_values):
    [update_id, item, cuerpo, chat_id, msg_id, tarea, usuario] = updater_values
    updates = telegram.get_updates(offset=update_id)
    updates = updates["result"]
    if len(updates) != 0:
        logging.info(updates)
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                if "message" in item:
                    cuerpo = item["message"]
                    chat_id = cuerpo["chat"]["id"]
                    msg_id = cuerpo["message_id"]
                    if cuerpo["text"].lower() == "/start":
                        logging.info("Wake up protocol, let's check if is someone known")
                        client_id = cuerpo["from"]["id"]
                        if get_client_info(str(client_id)):
                            cliente = get_client_info(str(client_id))
                            usuario = [client_id, cliente["nombre"], cliente["password"]]
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
                        elif tarea == "password":
                            password = cuerpo["text"].lower()
                            usuario[2] = password  # contraseña, necesaria validacion de long, caracteres...
                            tarea = "reg_hab"
                        elif tarea == "hab":
                            habitacion = cuerpo["text"].lower()
                            usuario[3] = habitacion
                            tarea = "registro_completado"
                        elif tarea == "nohab":
                            habitacion = None
                            usuario[3] = habitacion
                            tarea = "registro_completado"
                        else:
                            mensaje = cuerpo["text"].lower()

                elif "callback_query" in item:
                    cuerpo = item["callback_query"]["message"]
                    chat_id = cuerpo["chat"]["id"]
                    msg_id = item["callback_query"]["message"]["message_id"]
                    tarea = item["callback_query"]["data"]
                    if tarea == "atras":
                        usuario = [None, None, None]
                elif "edited_message" in item:
                    cuerpo = item["edited_message"]     # a partir de aqui copy paste de message
                    chat_id = cuerpo["chat"]["id"]
                    msg_id = cuerpo["message_id"]
                    if cuerpo["text"].lower() == "/start":
                        logging.info("Wake up protocol, let's check if is someone known")
                        client_id = cuerpo["from"]["id"]

                        if get_client_info(str(client_id)):
                            cliente = get_client_info(str(client_id))
                            usuario = [client_id, cliente["nombre"], ["password"]]
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
                            print(usuario)
                        elif tarea == "password":
                            password = cuerpo["text"].lower()
                            usuario[2] = password  # contraseña, necesaria validacion de long, caracteres...
                            tarea = "reg_hab"
                        elif tarea == "hab":
                            habitacion = cuerpo["text"].lower()
                            usuario[3] = habitacion
                            tarea = "registro_completado"
                        elif tarea == "nohab":
                            habitacion = None
                            usuario[3] = habitacion
                            tarea = "registro_completado"
                        else:
                            mensaje = cuerpo["text"].lower()
                else:  # solucion temporal

                    cuerpo = item
                    chat_id = None
                    tarea = "No_se"
                    msg_id = chat_id

                if "text" in cuerpo and cuerpo["text"].lower() == "/adios":
                    tarea = "texto"
                    print()  # reiniciariamos el bot para otra ocasion

            except:
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
    updater_values = [update_id, item, cuerpo, chat_id, msg_id, tarea, usuario]
    return updater_values
