from app.logica.helpers import (
    limpiar_texto,
    duracion_en_minutos,
    horario_en_minutos,
    sacar_hora_horario,
)
from app.logica.json_access import cargar_json, guardar_json


# Buscar peliculas
def buscar_peliculas(busqueda=None, categoria=None, duracion=None):
    peliculas = cargar_json("peliculas.json")
    funciones = cargar_json("funciones.json")
    con_funcion = {int(f["pelicula_id"]) for f in funciones.values()}
    resultados = [p for p in peliculas if int(p["id"]) in con_funcion]

    if busqueda:
        b = limpiar_texto(busqueda)
        resultados = list(filter(lambda p: b in limpiar_texto(p["titulo"]), resultados))


    if categoria:
        cat = limpiar_texto(categoria)
        resultados = [
            p for p in resultados
            if any(cat in limpiar_texto(str(c)) for c in p["categoria"])
     ]


    if duracion:

        def mins(p):
            return duracion_en_minutos(p["duracion"])

        if duracion == "corta":
            resultados = [p for p in resultados if mins(p) < 100]
        elif duracion == "media":
            resultados = [p for p in resultados if 100 <= mins(p) <= 150]
        elif duracion == "larga":
            resultados = [p for p in resultados if mins(p) > 150]

    return resultados


# Agregar funcion admin
def agregar_funcion(pelicula_id, sala, fecha, hora, idioma):
    funciones = cargar_json("funciones.json")
    salas = cargar_json("salas.json")
    if not comprobar_funciones(int(pelicula_id), sala, fecha, hora):
        return
    filas = salas[sala]["filas"]
    columnas = salas[sala]["columnas"]
    nueva_id = str(len(funciones) + 1)
    funciones[nueva_id] = {
        "pelicula_id": int(pelicula_id),
        "sala": sala,
        "fecha": fecha,
        "hora": hora,
        "idioma": idioma,
        "asientos": [[0] * columnas for _ in range(filas)],
    }
    guardar_json(funciones, "funciones.json")


# Comprobar conflictos de funciones
def comprobar_funciones(pelicula_id, sala, fecha, hora):
    peliculas = cargar_json("peliculas.json")
    funciones = cargar_json("funciones.json")

    def buscar_pelicula(pid):
        for p in peliculas:
            if int(p["id"]) == int(pid):
                return p
        return None

    pelicula = buscar_pelicula(pelicula_id)
    if pelicula is None:
        print("Película no encontrada.")
        return False

    duracion_total = duracion_en_minutos(pelicula["duracion"])
    minutos_nueva = horario_en_minutos(hora)
    fin_funcion_nueva = minutos_nueva + duracion_total
    h = sacar_hora_horario(hora)

    if 2 <= h < 16:
        print("No se pueden agendar funciones entre las 02:00 y las 16:00.")
        return False

    for f in funciones.values():

        if f["sala"] == sala and f["fecha"] == fecha:

            pelicula_existente = buscar_pelicula(f["pelicula_id"])
            if pelicula_existente is None:
                continue

            minutos_existente = horario_en_minutos(f["hora"])
            duracion_existente = duracion_en_minutos(pelicula_existente["duracion"])
            fin_funcion_existente = minutos_existente + duracion_existente

            if not (
                fin_funcion_nueva <= minutos_existente
                or fin_funcion_existente <= minutos_nueva
            ):
                print(f"Conflicto con función que termina a las {f['hora']}.")
                return False

    return True

# Encontrar funciones por id de pelicula
def encontrar_funciones(pelicula_id):
    funciones = cargar_json("funciones.json")
    return [
        {"id": fid, **f}
        for fid, f in funciones.items()
        if int(f["pelicula_id"]) == int(pelicula_id)
    ]

# Encontrar pelicula por id
def encontrar_peliculas(lista, pid):
    for p in lista:
        if int(p["id"]) == int(pid):
            return p
    return None

# Mostrar valores de funciones
def obtener_funciones(funciones, fecha=None, idioma=None):
    fechas = {f["fecha"] for f in funciones}

    if fecha:
        filtradas_fecha = filter(lambda f: f["fecha"] == fecha, funciones)
        idiomas = {f["idioma"] for f in filtradas_fecha}
    else:
        idiomas = {f["idioma"] for f in funciones}

    if fecha and idioma:
        filtradas = filter(
            lambda f: f["fecha"] == fecha and f["idioma"] == idioma,
            funciones
        )
        horarios = {f["hora"] for f in filtradas}
    else:
        horarios = set()

    return list(fechas), list(idiomas), list(horarios)

<<<<<<< HEAD
# Butacas


from pathlib import Path
import json

salas_ruta = Path("app/data/salas.json")


def cargar_salas():
    with open(salas_ruta, encoding="utf-8") as f:
        return json.load(f)


def obtener_o_crear_butacas_por_funcion(funcion: dict, salas: dict) -> list[list[int]]:
    sala_id = funcion.get("sala")

    if sala_id is None:
        raise ValueError("La función seleccionada no tiene sala asignada")

    sala_cfg = salas.get(sala_id)
    if sala_cfg is None:
        raise ValueError(f"Sala '{sala_id}' no definida en salas.json")

    filas = sala_cfg["filas"]
    columnas = sala_cfg["columnas"]

    
    if not funcion.get("asientos"):
        funcion["asientos"] = [[0 for _ in range(columnas)] for _ in range(filas)]

    return funcion["asientos"]


def reservar_butaca_funcion(funciones, funcion_id, fila, columna):
    salas = cargar_salas()
    funcion = funciones.get(str(funcion_id))

    if not funcion:
        return {"ok": False, "msg": "La función no existe"}

    asientos = obtener_o_crear_butacas_por_funcion(funcion, salas)

    f_idx = fila - 1
    c_idx = columna - 1

    
    if f_idx < 0 or c_idx < 0 or f_idx >= len(asientos) or c_idx >= len(asientos[0]):
        return {"ok": False, "msg": "La butaca no existe en esta sala"}

    # Ocupada
    if asientos[f_idx][c_idx] == 1:
        return {"ok": False, "msg": "La butaca ya está ocupada"}

    # Reservar
    asientos[f_idx][c_idx] = 1
    return {"ok": True, "msg": "Reserva exitosa"}
=======
>>>>>>> 7bc56f05cd185530bee17afeb281c6921802c2af
