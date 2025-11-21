import json
from json import JSONDecodeError
from pathlib import Path

def cargar_json(nombre):
    ruta = Path("app/data") / nombre

    try: #A1
        with ruta.open("r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError as e:
        registrar_error(e)
        return {}

    except JSONDecodeError as e:
        registrar_error(e)
        return {}


# Guardar
def guardar_json(data, nombre):
    ruta = Path("app/data") / nombre

    try:
        with ruta.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        registrar_error(e)
        print(f"Error al guardar JSON en {ruta}")

def registrar_error(e):
    with open("errores.log", "a") as log:
        linea = f"Tipo: {type(e)} | Mensaje: {str(e)}\n"
        log.write(linea)