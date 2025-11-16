from app.logica.helpers import (
    limpiar_texto,
    duracion_en_minutos,
    horario_en_minutos,
    sacar_hora_horario,
)
from app.logica.json_access import (
    cargar_peliculas,
    cargar_funciones,
    cargar_salas,
    guardar_funciones,
)


def buscar_peliculas(busqueda=None, categoria=None, duracion=None):
    peliculas = cargar_peliculas()
    funciones = cargar_funciones()
    con_funcion = {int(f["pelicula_id"]) for f in funciones.values()}
    resultados = [p for p in peliculas if int(p["id"]) in con_funcion]

    if busqueda:
        b = limpiar_texto(busqueda)
        filtrados = []
        for p in resultados:
            if b in limpiar_texto(p["titulo"]):
                filtrados.append(p)
        resultados = filtrados

    if categoria:
        cat = limpiar_texto(categoria)
        filtrados = []
        for p in resultados:
            for c in p["categoria"]:
                if cat in limpiar_texto(str(c)):
                    filtrados.append(p)
                    break
        resultados = filtrados

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


def agregar_funcion(pelicula_id, sala, fecha, hora, idioma):
    funciones = cargar_funciones()
    salas = cargar_salas()
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
    guardar_funciones(funciones)


def comprobar_funciones(pelicula_id, sala, fecha, hora):
    peliculas = cargar_peliculas()
    funciones = cargar_funciones()
    pelicula = None
    for p in peliculas:
        if int(p["id"]) == int(pelicula_id):
            pelicula = p
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
            pelicula_existente = None
            for p in peliculas:
                if int(p["id"]) == int(f["pelicula_id"]):
                    pelicula_existente = p
            if pelicula_existente is not None:
                minutos_existente = horario_en_minutos(f["hora"])
                duracion_existente = duracion_en_minutos(pelicula_existente["duracion"])
                fin_funcion_existente = minutos_existente + duracion_existente
                if not (fin_funcion_nueva <= minutos_existente or fin_funcion_existente <= minutos_nueva):
                    print(f"Conflicto con función que termina a las {f['hora']}.")
                    return False
    return True


def encontrar_funciones(pelicula_id):
    funciones = cargar_funciones()
    lista = []
    for fid, f in funciones.items():
        if int(f["pelicula_id"]) == int(pelicula_id):
            lista.append({"id": fid, **f})
    return lista


def encontrar_peliculas(pid):
    peliculas = cargar_peliculas()
    for p in peliculas:
        if int(p["id"]) == int(pid):
            return p
    return None


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
            if (
                f["fecha"] == fecha
                and f["idioma"] == idioma
                and f["hora"] not in horarios
            ):
                horarios.append(f["hora"])
    return fechas, idiomas, horarios
