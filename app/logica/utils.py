import json
import string
import unicodedata
import bcrypt
from pathlib import Path
from datetime import datetime


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
    funciones = cargar_funciones()
    salas = cargar_salas()
    filas = salas[sala]["filas"]
    columnas = salas[sala]["columnas"]
    nueva_id = f"funcion{len(funciones) + 1}"
    funciones[nueva_id] = {
        "pelicula_id": pelicula_id,
        "sala": sala,
        "fecha": fecha,
        "hora": hora,
        "idioma": idioma,
        "asientos": [
            [0 for _ in range(columnas)] for _ in range(filas)
        ],
    }
    guardar_funciones(funciones)


# Encryptar contraseña
password = ""
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())


# Mostrar funciones
def encontrar_funciones(pelicula_id):
    funciones = cargar_funciones()
    return [
        {"id": fid, **f}
        for fid, f in funciones.items()
        if str(f["pelicula_id"]) == str(pelicula_id)
    ]


# Mostrar peliculas
def encontrar_peliculas(id: int):
    pelicula = peliculas.get(str(id))
    if pelicula:
        pelicula_con_id = dict(pelicula)
        pelicula_con_id["id"] = id
        return pelicula_con_id
    return None


# Filtros de peliculas
def buscar_peliculas(
    busqueda: str | None, categoria: str | None = None, duracion: str | None = None
):
    funciones = cargar_funciones()
    resultados = []

    resultados = [{**pelicula, "id": id} for id, pelicula in peliculas.items()]
    peliculas_con_funcion = {f["pelicula_id"] for f in funciones.values()}
    resultados = [pelicula for pelicula in resultados if str(pelicula["id"]) in peliculas_con_funcion]

    if categoria:
        categoria_filtrada = quitar_tildes(categoria.lower())
        resultados = [
            pelicula
            for pelicula in resultados
            if categoria_filtrada in quitar_tildes(str(pelicula["categoria"]).lower())
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


# Normalizar texto quitando tildes
def quitar_tildes(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFD", texto)
    texto_sin_tildes = "".join(
        c for c in texto_normalizado if unicodedata.category(c) != "Mn"
    )
    return texto_sin_tildes


# Normalizar texto quitando signo de puntuación y demas
def quitar_punt(texto: str) -> str:
    return texto.translate(str.maketrans("", "", string.punctuation))


# Precios
def precio_por_estreno(fecha_lanzamiento):
    precio_estandar = 7999
    precio_estreno = precio_estandar * 1.35
    hoy = datetime.now()
    dias_estreno = (hoy - fecha_lanzamiento).days
    return precio_estandar if dias_estreno >= 7 else precio_estreno


def formatear_moneda(valor):
    entero, dec = f"{valor:,.2f}".split(".")
    return f"$ {entero.replace(',', '.')},{dec}"


def precio_por_perfil(edad, movistar):
    precio_estandar = 7999
    precio_movistar = 7500
    precio_reducido = 6999
    if edad > 65:
        return "Jubilado", formatear_moneda(precio_reducido)
    elif edad < 6:
        return "Menor", formatear_moneda(precio_reducido)
    elif movistar == 1:
        return "Movistar", formatear_moneda(precio_movistar)
    else:
        return "Entrada", formatear_moneda(precio_estandar)

# Seleccion de funciones
def obtener_funciones(funciones, fecha=None, idioma=None):
    fechas = []
    idiomas = []
    horarios = []

    for f in funciones:
        if f["fecha"] not in fechas:
            fechas.append(f["fecha"])

    if fecha:
        for f in funciones:
            if f["fecha"] == fecha and f["idioma"] not in idiomas:
                idiomas.append(f["idioma"])

    if fecha and idioma:
        for f in funciones:
            if f["fecha"] == fecha and f["idioma"] == idioma and f["hora"] not in horarios:
                horarios.append(f["hora"])

    return fechas, idiomas, horarios

# Cargar salas
salas_ruta = Path("app/data/salas.json")

def cargar_salas():
    with open(salas_ruta, encoding="utf-8") as f:
        return json.load(f)