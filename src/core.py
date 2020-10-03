import logging
from src.DB.DB_handler import *


def procesamiento_info(cuerpo, tarea, inicio, usuario=None):
    try:
        if not inicio:
            tarea = "texto"
        if tarea == "usuario":
            usuario[0] = cuerpo["from"]["id"]
            user = cuerpo["text"]
            usuario[1] = user  # nombre de usuario, necesaria validacion de nombre
        elif tarea == "g_password":
            password = cuerpo["text"]
            usuario[2] = password

        elif tarea == "g_hab":
            habitacion = cuerpo["text"].lower()
            usuario[3] = habitacion
            tarea = "reg_completado"

        elif tarea == "nohab":
            habitacion = None
            usuario[3] = habitacion
            tarea = "reg_completado"

        elif tarea == "reinicio_room":
            usuario[3] = None
            tarea = "reinicio"

        if tarea == "add_piso":
            if "text" in cuerpo:
                habitacion = cuerpo["text"].lower()
                reg_room(habitacion)

        elif tarea == "deleted_client":
            if "text" in cuerpo:
                cliente = cuerpo["text"].lower()
                delete_registro("clientes", cliente)

        elif tarea == "reg_completado":
            registro_db(usuario)

        if "text" in cuerpo and cuerpo["text"].lower() == "/adios":
            tarea = "texto"
            usuario = [None, None, None, None, "Public"]
            print()  # reiniciariamos el bot para otra ocasion
    except:
        logging.exception("error traceback from procesamiento")

    return usuario, tarea
