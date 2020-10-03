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
        logging.info("client already in database!")
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
    pisos_set = read_json("../src/DB/pisos.json")
    piso = {hab: {"ocupado": false}}
    pisos_set.update(piso)
    write_json("../src/DB/pisos.json", pisos_set)


def read_json(directory):
    with open(directory, "r", encoding='utf-8-sig') as data:
        archivo = json.loads(data.read())
    return archivo


def write_json(directory, archivo):
    with open(directory, "w", encoding='utf-8-sig') as data:
        data.write(json.dumps(archivo, sort_keys=True, indent=4, separators=(',', ': ')))
