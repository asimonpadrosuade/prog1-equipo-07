import json
import string
import unicodedata
import bcrypt
from pathlib import Path
from datetime import datetime, timedelta
from functools import lru_cache

peliculas_ruta = Path("app/data/peliculas.json")
usuarios_ruta = Path("app/data/usuarios.json")
funciones_ruta = Path("app/data/funciones.json")
salas_ruta = Path("app/data/salas.json")


@lru_cache()
def cargar_peliculas():
    with open(peliculas_ruta, encoding="utf-8") as f:
        return json.load(f)


@lru_cache()
def cargar_usuarios():
    with open(usuarios_ruta, encoding="utf-8") as f:
        return json.load(f)


@lru_cache()
def cargar_funciones():
    with open(funciones_ruta, encoding="utf-8") as f:
        return json.load(f)


@lru_cache()
def cargar_salas():
    with open(salas_ruta, encoding="utf-8") as f:
        return json.load(f)
    
def comprobar_admin(request):
    return request.cookies.get("admin") == "1"


def guardar_funciones(funciones):
    with open(funciones_ruta, "w", encoding="utf-8") as f:
        json.dump(funciones, f, ensure_ascii=False, indent=2)
    cargar_funciones.cache_clear()


def verificar_usuario(username, password):
    usuarios = cargar_usuarios()
    user = usuarios.get(username)
    return user and bcrypt.checkpw(password.encode(), user["password"].encode())


def duracion_en_minutos(d):
    horas, minutos = d.lower().replace("m", "").split("h")
    return int(horas.strip()) * 60 + int(minutos.strip())


def agregar_funcion(pelicula_id, sala, fecha, hora, idioma):
    funciones = cargar_funciones()
    salas = cargar_salas()
    peliculas = cargar_peliculas()

    pelicula = peliculas[str(pelicula_id)]
    dur_nueva = duracion_en_minutos(pelicula["duracion"]) + 30

    nueva_ini = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    nueva_fin = nueva_ini + timedelta(minutes=dur_nueva)

    for f in funciones.values():
        if f["sala"] == sala and f["fecha"] == fecha:
            existente_ini = datetime.strptime(f"{f['fecha']} {f['hora']}", "%Y-%m-%d %H:%M")
            dur_exist = duracion_en_minutos(peliculas[str(f["pelicula_id"])]["duracion"]) + 30
            existente_fin = existente_ini + timedelta(minutes=dur_exist)

            if existente_ini < nueva_fin and nueva_ini < existente_fin:
                raise ValueError(
                    f"Conflicto de horario: la función existente termina a las "
                    f"{existente_fin.strftime('%H:%M')}."
                )

    filas = salas[sala]["filas"]
    columnas = salas[sala]["columnas"]

    nueva_id = f"funcion{len(funciones) + 1}"
    funciones[nueva_id] = {
        "pelicula_id": pelicula_id,
        "sala": sala,
        "fecha": fecha,
        "hora": hora,
        "idioma": idioma,
        "asientos": [[0] * columnas for _ in range(filas)],
    }

    guardar_funciones(funciones)


def encontrar_funciones(pelicula_id):
    funciones = cargar_funciones()
    return [
        {"id": fid, **f}
        for fid, f in funciones.items()
        if str(f["pelicula_id"]) == str(pelicula_id)
    ]


def encontrar_peliculas(id):
    peliculas = cargar_peliculas()
    pelicula = peliculas.get(str(id))
    return {**pelicula, "id": id} if pelicula else None


def quitar_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def quitar_punt(t):
    return t.translate(str.maketrans("", "", string.punctuation))


def buscar_peliculas(busqueda=None, categoria=None, duracion=None):
    peliculas = cargar_peliculas()
    funciones = cargar_funciones()

    resultados = [{**p, "id": int(id)} for id, p in peliculas.items()]
    usadas = {f["pelicula_id"] for f in funciones.values()}
    resultados = [p for p in resultados if str(p["id"]) in usadas]

    if categoria:
        cat = quitar_tildes(categoria.lower())
        resultados = [p for p in resultados if cat in quitar_tildes(p["categoria"].lower())]

    if duracion:
        if duracion == "corta":
            resultados = [p for p in resultados if duracion_en_minutos(p["duracion"]) < 100]
        elif duracion == "media":
            resultados = [p for p in resultados if 100 <= duracion_en_minutos(p["duracion"]) <= 150]
        elif duracion == "larga":
            resultados = [p for p in resultados if duracion_en_minutos(p["duracion"]) > 150]

    return resultados


def precio_por_estreno(fecha_lanzamiento):
    base = 7999
    estreno = base * 1.35
    dias = (datetime.now() - fecha_lanzamiento).days
    return estreno if dias < 7 else base


def formatear_moneda(v):
    e, d = f"{v:,.2f}".split(".")
    return f"$ {e.replace(',', '.')},{d}"


def precio_por_perfil(edad, movistar):
    if edad > 65 or edad < 6:
        return "Jubilado/Menor", formatear_moneda(6999)
    if movistar == 1:
        return "Movistar", formatear_moneda(7500)
    return "Entrada", formatear_moneda(7999)


def obtener_funciones(funciones, fecha=None, idioma=None):
    fechas = {f["fecha"] for f in funciones}
    idiomas_disponibles = {f["idioma"] for f in funciones if f["fecha"] == fecha} if fecha else []
    horarios = {f["hora"] for f in funciones if f["fecha"] == fecha and f["idioma"] == idioma} if fecha and idioma else []
    return list(fechas), list(idiomas_disponibles), list(horarios)