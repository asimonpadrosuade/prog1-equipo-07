import json
import bcrypt
from pathlib import Path
from app.logica.json_access import cargar_json


# Cargar peliculas
peliculas_ruta = Path("app/data/peliculas.json")


def cargar_peliculas():
    with open(peliculas_ruta, encoding="utf-8") as f:
        return json.load(f)


peliculas = cargar_peliculas()

# Cargar usuarios
usuarios_ruta = Path("app/data/usuarios.json")


def cargar_usuarios():
    with open(funciones_ruta, encoding="utf-8") as f:
        return json.load(f)


# Verificar usuario
def verificar_usuario(username, password):
    with open(usuarios_ruta, encoding="utf-8") as f:
        usuarios = json.load(f)
    user = usuarios.get(username)
    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        return True
    return False


# Cargar funciones
funciones_ruta = Path("app/data/funciones.json")


def cargar_funciones():
    with open(funciones_ruta, encoding="utf-8") as f:
        return json.load(f)


# Guardar funciones
def guardar_funciones(funciones):
    with open(funciones_ruta, "w", encoding="utf-8") as f:
        json.dump(funciones, f, ensure_ascii=False, indent=2)


# Agregar funciones
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
        "asientos": [[0 for _ in range(columnas)] for _ in range(filas)],
    }
    guardar_funciones(funciones)


# Encryptar contraseña (solo para generar hashes)
password = ""
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())


# Mostrar funciones
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


# Filtros de peliculas
def buscar_peliculas(
    busqueda: str | None, categoria: str | None = None, duracion: str | None = None
):
    funciones = cargar_funciones()

    resultados = [{**pelicula, "id": i} for i, pelicula in enumerate(peliculas)]
    peliculas_con_funcion = {f["pelicula_id"] for f in funciones.values()}
    resultados = [
        pelicula
        for pelicula in resultados
        if str(pelicula["id"]) in peliculas_con_funcion
    ]

    if categoria:
        categoria_filtrada = categoria.lower()
        resultados = [
            pelicula
            for pelicula in resultados
            if categoria_filtrada in str(pelicula["categoria"]).lower()
        ]

    if duracion:

        def duracion_en_minutos(d: str) -> int:
            horas, minutos = d.split("h ")
            minutos = minutos.replace("m", "")
            return int(horas) * 60 + int(minutos)

        if duracion == "corta":
            resultados = [
                pelicula
                for pelicula in resultados
                if duracion_en_minutos(pelicula["duracion"]) < 100
            ]
        elif duracion == "media":
            resultados = [
                pelicula
                for pelicula in resultados
                if 100 <= duracion_en_minutos(pelicula["duracion"]) <= 150
            ]
        elif duracion == "larga":
            resultados = [
                pelicula
                for pelicula in resultados
                if duracion_en_minutos(pelicula["duracion"]) > 150
            ]

    return resultados


# Precios fijos por tipo de entrada
PRECIOS = {"comun": 15000, "menor_jubilado": 10000, "movistar": 15000}


# Seleccion de funciones (fechas, idiomas, horarios)
def obtener_funciones(funciones, fecha=None, idioma=None):
    fechas = [f["fecha"] for f in funciones]
    fechas = list(dict.fromkeys(fechas))

    if fecha:
        idiomas_disponibles = [
            f["idioma"] for f in funciones if f["fecha"] == fecha
        ]
        idiomas_disponibles = list(dict.fromkeys(idiomas_disponibles))
    else:
        idiomas_disponibles = []

    if fecha and idioma:
        horarios = [
            f["hora"]
            for f in funciones
            if f["fecha"] == fecha and f["idioma"] == idioma
        ]
        horarios = list(dict.fromkeys(horarios))
    else:
        horarios = []

    return list(fechas), list(idiomas_disponibles), list(horarios)


# Cargar salas
salas_ruta = Path("app/data/salas.json")


def cargar_salas():
    with open(salas_ruta, encoding="utf-8") as f:
        return json.load(f)
