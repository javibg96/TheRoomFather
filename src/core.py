import logging
from src.DB.DB_handler import *


def procesamiento_info(cuerpo, tarea, usuario=None):

    print(tarea)
    print(cuerpo["text"])
    if tarea == "registro":
        usuario[0] = cuerpo["from"]["id"]
        user = cuerpo["text"]
        usuario[1] = user  # nombre de usuario, necesaria validacion de nombre
        tarea = "password"
    elif "password" in tarea:
        password = cuerpo["text"].lower()
        if check_password(password):
            usuario[2] = password
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

    elif tarea == "registro_completado":
        registro_db(usuario)

    if "text" in cuerpo and cuerpo["text"].lower() == "/adios":
        tarea = "texto"
        usuario = [None, None, None, None]
        print()  # reiniciariamos el bot para otra ocasion

    return usuario, tarea


