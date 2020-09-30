from src.telegram_api_handler import TelegramApi
from src.DB.DB_handler import registro_db


def send_initial_menu(chat_id):
    pregunta = "Bienvenido a nuestro bot de ayuda, encantado de conocerte, ¿Qué quieres hacer?"
    keyBoard = '{"inline_keyboard": [[{"text": "Registro", "callback_data": "registro"}], [{"text": "otro", ' \
               '"callback_data": "otro"}]]} '
    TelegramApi().send_message(pregunta, chat_id, keyBoard)


def registro(chat_id, msg_id, option):
    keyBoard = '{"inline_keyboard":[[{"text": "<< Atrás", "callback_data": "texto"}]]}'
    if option == "registro":
        texto = "escriba nombre de usuario"
        TelegramApi().edit_message(msg_id, chat_id, texto, keyBoard)
    elif option == "password":
        texto = "nombre de usuario guardado, ahora elija su contraseña"
        TelegramApi().send_message(texto, chat_id)
    elif option == "reg_hab":
        TelegramApi().delete_message(chat_id, msg_id)
        texto = "Contraseña almacenada, ¿Tiene alquilada alguna habitación con nosotros?"
        keyBoard = '{"inline_keyboard":[[{"text": "Si", "callback_data": "hab"}],' \
                   '[{"text": "No", "callback_data":"nohab"}]]} '
        TelegramApi().send_message(texto, chat_id, keyBoard)
    elif option == "hab":
        texto = "Introduzca por favor la direccion del piso"
        TelegramApi().edit_message(msg_id, chat_id, texto)
    else:
        texto = "Datos almacenados en nuestra base de datos"
        TelegramApi().edit_message(msg_id, chat_id, texto)


def registered_client_menu(chat_id, option, client_name=None):
    keyBoard = '{"inline_keyboard": [[{"text": "Registrar piso", "callback_data": "reg_hab"}], [{"text": "Limpiar ' \
               'piso", "callback_data": "limpieza"}], [{"text": "Necesario arreglo", "callback_data": "arreglos"}],' \
               '[{"text": "Otro", "callback_data": "otro"}]]} '
    if option == "registro_completado":
        pregunta = "¿Qué quieres hacer ahora?"
        texto = "Nombre de usuario y contraseña guardados, registro completado, Muchas gracias"
        TelegramApi().send_message(texto, chat_id)
    else:
        pregunta = f"Hola de nuevo {client_name},¿Qué quieres hacer ahora?"

    TelegramApi().send_message(pregunta, chat_id, keyBoard)


def registered_room_menu(chat_id, msg_id, option):
    pregunta = "¿Qué quieres hacer ahora?"
    keyBoard = '{"inline_keyboard": [[{"text": "Limpieza piso", "callback_data": "limpieza"}], ' \
               '[{"text": "Necesario arreglo", "callback_data": "arreglos"}], ' \
               '[{"text": "Otro", "callback_data": "log-in"}]]} '
    if option == "registro_completado":
        TelegramApi().delete_message(chat_id, msg_id)
        texto = "Nombre de usuario y contraseña guardados, registro completado, Muchas gracias"
        TelegramApi().send_message(texto, chat_id)
        TelegramApi().send_message(pregunta, chat_id, keyBoard)
    else:
        TelegramApi().edit_message(msg_id, chat_id, pregunta, keyBoard)


def menu_handler(cuerpo, chat_id, msg_id, tarea, user):
    print(tarea)
    lista_tareas = ["registro", "password", "log-in", "limpieza", "atras", "otro", "registro_completado"]
    if tarea == "texto":
        send_initial_menu(chat_id)
    else:
        if tarea == "registro_completado":
            registro_db(user)
            option_selector(chat_id, msg_id, tarea)
        elif tarea == "cliente_registrado":
            nombre = user[1]
            option_selector(chat_id, msg_id, tarea, nombre)
        else:
            option_selector(chat_id, msg_id, tarea)
    try:
        if cuerpo["text"]:
            message = cuerpo["text"].lower()
        else:
            message = "un mensaje que no se que es"
    except:
        print(cuerpo)


def option_selector(chat_id, msg_id, option, nombre=None):
    if option in ["registro", "password", "reg_hab", "hab", "nohab"]:
        registro(chat_id, msg_id, option)

    elif option in ["atras", "registro_completado"]:
        registered_client_menu(chat_id, option)
    elif option == "cliente_registrado":
        print(nombre)
        registered_client_menu(chat_id, option, nombre)
    else:
        if option == "limpieza":
            texto = "¿Que cantidad de horas necesita?"
            keyBoard = '{"inline_keyboard": [[{"text": "2 horas", "callback_data": 2}], ' \
                       '[{"text": "4 horas", "callback_data": 4}], ' \
                       '[{"text": "6 horas", "callback_data": 6}], ' \
                       '[{"text": "<< Atrás", "callback_data": "atras"}]]} '
        elif option.isdigit():  # horas de limpieza
            texto = f"Perfecto, ahora mismo enviamos a un equipo para que limpie {option} horas, buen dia"
            keyBoard = None

        else:
            texto = "escriba en que puedo ayudarle a ver si puedo encontrar alguna solución"
            keyBoard = '{"inline_keyboard":[{"text": "<< Atrás", "callback_data": "atras"}]]}'

        TelegramApi().edit_message(msg_id, chat_id, keyBoard, texto)
