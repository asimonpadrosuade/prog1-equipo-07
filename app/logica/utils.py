import json
from pathlib import Path
import string
import unicodedata
from datetime import datetime

# Cargar peliculas
peliculas_ruta = Path("app/data/peliculas.json")
def cargar_peliculas():
    with open(peliculas_ruta, encoding="utf-8") as f:
        return json.load(f)

#Cargar funciones
funciones_ruta = Path("app/data/funciones.json")
def cargar_funciones():
    with open(funciones_ruta, encoding="utf-8") as f:
        return json.load(f)
    
#Guardar funciones
def guardar_funciones(funciones):
    with open(funciones_ruta, "w", encoding="utf-8") as f:
        json.dump(funciones, f, ensure_ascii=False, indent=2)

peliculas = cargar_peliculas()

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
    
    resultados=[]
    resultados = [{**pelicula, "id": id} for id, pelicula in peliculas.items()]



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
    return texto.translate(str.maketrans('', '', string.punctuation))


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


# Butacas