import string
import unicodedata
from datetime import datetime
from app.data.peliculas import peliculas

# Mostrar peliculas
def encontrar_peliculas(id: int):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            return pelicula
    return None

# Filtros de peliculas
def buscar_peliculas(
    busqueda: str | None, categoria: str | None = None, duracion: str | None = None
):
    resultados = peliculas

    if busqueda:
        resultados = [
            pelicula
            for pelicula in resultados
            if busqueda.lower() in quitar_tildes(quitar_punt(pelicula["titulo"].lower()))
        ]

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
def mostrar_sala(butacas):
    print("Sala:")
    for fila in butacas:
        for asiento in fila:
            print("O" if asiento == 0 else "X", end=" ")
        print()
    print()


def reservar_butaca(butacas, f, c):
    if butacas[f][c] == 0:
        butacas[f][c] = 1
        print(f"Butaca ({f + 1}, {c + 1}) reservada ")
    else:
        print(f"Butaca ({f + 1}, {c + 1}) ocupada")


filas = 5
columnas = 8
butacas = [[0 for _ in range(columnas)] for _ in range(filas)]
