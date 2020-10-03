import json
import logging


def check_room_availability(piso):
    exist = False
    pisos_set = read_json("../src/DB/pisos.json")
    if piso in pisos_set:
        exist = True
    return exist


def check_password(password):
    correct = False
    if len(password) >= 6:
        correct = True
    return correct


def check_client_info(client_id):
    clients_set = read_json("../src/DB/clientes.json")
    if client_id in clients_set:
        return clients_set[client_id]


def get_client_info(client_id):
    if check_client_info(client_id):
        cliente = check_client_info(client_id)
        usuario = [client_id, cliente["nombre"], cliente["password"], cliente["piso"], cliente["permiso"]]
        tarea = "cliente_registrado"
        return usuario, tarea


def registro_db(usuario):
    [client_id, user, password, hab] = usuario
    clients_set = read_json("../src/DB/clientes.json")
    cliente = {str(client_id): {"nombre": user, "permiso": "Public", "password": password, "piso": hab.lower()}}
    clients_set.update(cliente)
    write_json("../src/DB/clientes.json", clients_set)
    print(f"cliente {user} añadido")

    pisos_set = read_json("../src/DB/pisos.json")
    pisos_set[hab]["ocupado"] = True
    write_json("../src/DB/pisos.json", pisos_set)


def checkout(usuario):
    [client_id, user, password, hab] = usuario
    cliente = {client_id: {"nombre": user, "permiso": "Public", "password": password, "piso": None}}

    clients_set = read_json("../src/DB/clientes.json")
    clients_set.update(cliente)
    write_json("../src/DB/clientes.json", clients_set)

    pisos_set = read_json("../src/DB/pisos.json")
    pisos_set[hab]["ocupado"] = False
    write_json("../src/DB/pisos.json", pisos_set)
    print(f"Piso {hab} liberado")


def reg_room(hab):
    try:
        pisos_set = read_json("../src/DB/pisos.json")
        piso = {hab: {"ocupado": False}}
        pisos_set.update(piso)
        print(pisos_set)
        write_json("../src/DB/pisos.json", pisos_set)
    except:
        logging.exception("error in reg_room traceback")


def show_clients():
    clients_set = read_json("../src/DB/clientes.json")
    nombre_clientes = []
    for cliente in clients_set.keys():
        nombre_clientes.append(clients_set[cliente]["nombre"])
    return nombre_clientes


def delete_registro(db, registro):
    print(f"REGISTROOO {registro}")
    reg_found = False
    deleted_id = 0
    directory = f"../src/DB/{db}.json"
    registro_set = read_json(directory)
    if registro in registro_set:
        registro_set.pop(registro)
    else:
        for element in registro_set.keys():
            if registro == registro_set[element]["nombre"].lower():
                reg_found = True
                deleted_id = element
    if reg_found:
        print(registro_set[deleted_id]["nombre"])
        registro_set.pop(deleted_id)
    write_json(directory, registro_set)


def read_json(directory):
    with open(directory, "r", encoding='utf-8-sig') as data:
        archivo = json.loads(data.read())
    return archivo


def write_json(directory, archivo):
    with open(directory, "w", encoding='utf-8-sig') as data:
        data.write(json.dumps(archivo, sort_keys=True, indent=4, separators=(',', ': ')))
