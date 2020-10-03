from src.telegram_api_handler import TelegramApi
from src.DB.DB_handler import registro_db, checkout, get_client_info


def initial_menu(chat_id):
    pregunta = "Bienvenido a nuestro bot de ayuda, encantado de conocerte, ¿Qué quieres hacer?"
    keyBoard = '{"inline_keyboard": [[{"text": "Registro", "callback_data": "registro"}], [{"text": "otro", ' \
               '"callback_data": "otro"}]]} '
    TelegramApi().send_message(pregunta, chat_id, keyBoard)


def admin_menu(chat_id):
    pregunta = "ADMIN MENU -- ¿Qué quieres hacer?"
    keyBoard = '{"inline_keyboard": [[{"text": "Registrar propiedad", "callback_data": "reg_piso"}], ' \
               '[{"text": "Eliminar cliente", "callback_data": "delete_client"}],' \
               '[{"text": "Informe semanal", "callback_data": "informe"}]]} '
    TelegramApi().send_message(pregunta, chat_id, keyBoard)


def registro(chat_id, msg_id, option):
    keyBoard = '{"inline_keyboard":[[{"text": "<< Atrás", "callback_data": "texto"}]]}'
    if option == "registro":
        texto = "escriba nombre de usuario"
        TelegramApi().edit_message(msg_id, chat_id, texto, keyBoard)
    elif option == "usuario":
        texto = "nombre de usuario guardado, ahora elija su contraseña"
        TelegramApi().send_message(texto, chat_id)
    elif option == "n_password":
        texto = "escriba su antigua contraseña"
        TelegramApi().send_message(texto, chat_id)
    elif option == "act_password":
        texto = "escriba su nueva contraseña"
        TelegramApi().edit_message(msg_id, chat_id, texto)
    elif option == "w_password":
        texto = "contraseña no válida, intentelo de nuevo (la contraseña debe contener al menos 6 caracteres)"
        TelegramApi().send_message(texto, chat_id)
    elif option == "g_password":
        TelegramApi().delete_message(chat_id, msg_id)   # en siguiente version cambiar esto por editar contraseña por *
        texto = "Contraseña almacenada, ¿Tiene alquilada alguna habitación con nosotros?"
        keyBoard = '{"inline_keyboard":[[{"text": "Si", "callback_data": "hab"}],' \
                   '[{"text": "No", "callback_data":"nohab"}]]} '
        TelegramApi().send_message(texto, chat_id, keyBoard)
    elif option == "hab":
        texto = "Introduzca por favor la direccion del piso (ej. calle menganito 1)"
        TelegramApi().edit_message(msg_id, chat_id, texto)
    elif option == "w_hab":
        texto = "Dirección del piso introducida no valida, intentelo de nuevo por favor"
        TelegramApi().send_message(texto, chat_id)
    else:
        texto = "Datos almacenados en nuestra base de datos"        # registro completado
        TelegramApi().edit_message(msg_id, chat_id, texto)


def registered_client_menu(chat_id, tarea, room, client_name=None):
    if room:
        keyBoard = '{"inline_keyboard": [[{"text": "Dejar piso (Check out)", "callback_data": "check_out"}], ' \
                   '[{"text": "Limpiar piso", "callback_data": "limpieza"}], ' \
                   '[{"text": "Necesario arreglo", "callback_data": "arreglos"}],' \
                   '[{"text": "actualizar contraseña", "callback_data": "act_pass"}],' \
                   '[{"text": "Otro", "callback_data": "otro"}]]} '
    else:
        keyBoard = '{"inline_keyboard": [[{"text": "Estoy alquilando un piso", "callback_data": "hab"}],' \
                   '[{"text": "actualizar contraseña", "callback_data": "act_pass"}],' \
                   '[{"text": "Otro", "callback_data": "otro"}]]} '
    if tarea == "new_cliente_registrado":
        pregunta = "¿Qué quieres hacer ahora?"
        texto = "Registro completado, Muchas gracias"
        TelegramApi().send_message(texto, chat_id)
    else:
        pregunta = f"Hola de nuevo {client_name}, ¿Qué quieres hacer ahora?"

    TelegramApi().send_message(pregunta, chat_id, keyBoard)


def menu_handler(chat_id, msg_id, option, usuario):
    print(f"menu option: {option}")

    if option == "inicio":
        initial_menu(chat_id)

    if option == "inicio_admin":
        TelegramApi().delete_message(chat_id, msg_id)
        admin_menu(chat_id)

    elif option == "registro" or "password" in option or "usuario" in option or option in ["hab", "w_hab", "nohab"]:
        registro(chat_id, msg_id, option)

    elif option in ["reinicio", "cliente_registrado", "atras", "new_cliente_registrado"]:
        if option == "atras" or option == "reinicio":
            TelegramApi().delete_message(chat_id, msg_id)
            usuario = get_client_info(usuario[0])[0]
        registered_client_menu(chat_id, option, usuario[3], usuario[1])

    elif option == "g_hab":
        texto = "Datos almacenados, Registro completado."
        TelegramApi().send_message(texto, chat_id)
        usuario[3] = "Piso temporal"        # se coloca el de verdad al llegar a la siguiente funcion
        print(usuario)
        registered_client_menu(chat_id, option, usuario[3], usuario[1])

    elif option == "add_piso":
        texto = "Piso añadido con exito a la base de datos"
        keyBoard = '{"inline_keyboard":[[{"text": "<< Atrás", "callback_data": "inicio_admin"}]]}'
        TelegramApi().send_message(texto, chat_id, keyBoard)

    else:
        keyBoard = '{"inline_keyboard":[[{"text": "<< Atrás", "callback_data": "reinicio"}]]}'

        if option == "limpieza":
            texto = "¿Que cantidad de horas necesita?"
            keyBoard = '{"inline_keyboard": [[{"text": "1 hora", "callback_data": "1"}], ' \
                       '[{"text": "2 horas", "callback_data": "2"}],' \
                       '[{"text": "3 horas", "callback_data": "3"}]]}'

        elif option == "arreglos":
            texto = "¿Que tipo de arreglo necesita?"
            keyBoard = '{"inline_keyboard": [[{"text": "Fontanero", "callback_data": "fontanero"}], ' \
                       '[{"text": "Electricista", "callback_data": "electricista"}],' \
                       '[{"text": "Pintor", "callback_data": "pintor"}],' \
                       '[{"text": "Cerrajero", "callback_data": "cerrajero"}]]}'

        elif option in ["fontanero", "electricista", "pintor", "cerrajero"]:
            texto = f"en seguida mandamos a un {option} a su domicilio, que tenga un bien día"

        elif option.isdigit():  # horas de limpieza
            texto = f"Perfecto, ahora mismo enviamos a un equipo para que limpie {option} horas, buen dia"

        elif option == "check_out":     # mini bug en pasar de reg completado a check out, revisar
            checkout(usuario)
            texto = "Perfecto, ya hemos actualizado la base de datos, que tenga un buen día"
            keyBoard = '{"inline_keyboard":[[{"text": "<< Atrás", "callback_data": "reinicio"}]]}'

        elif option == "reg_piso":
            texto = "Introduce la direccion del piso a añadir"
            keyBoard = '{"inline_keyboard":[[{"text": "<< Atrás", "callback_data": "inicio_admin"}]]}'

        else:
            texto = "Escriba en que puedo ayudarle a ver si puedo encontrar alguna solución"

        TelegramApi().edit_message(msg_id, chat_id, texto, keyBoard)


