from datetime import datetime

#Precios
def precio_pelicula(fecha_lanzamiento):
    precio_estandar = 7999
    precio_estreno = precio_estandar * 1.35
    hoy = datetime.now()
    dias_estreno = (hoy - fecha_lanzamiento).days
    return precio_estandar if dias_estreno >= 7 else precio_estreno

#Butacas
def mostrar_sala(butacas):
    print("Sala:")
    for fila in butacas:
        for asiento in fila:
            if asiento == 0:
                print("O", end=" ")
            else:
                print("X", end=" ")
        print()
    print()

def reservar_butaca(butacas, f, c):
    if butacas[f][c] == 0:
        butacas[f][c] = 1
        print(f"Butaca ({f + 1}, {c + 1}) reservada ")
    else:
        print(f"Butaca ({f + 1}, {c + 1}) ocupada")

def ocultar_frame(frame):
    frame.pack_forget()

def mostrar_frame(frame, **kwargs):
    frame.pack(**kwargs)

from datetime import datetime
import unicodedata, re

def tiene_fechas(peli):
    fechas = peli.get("fechas")
    return isinstance(fechas, dict) and len(fechas) > 0

def tiene_horarios(peli):
    horarios = peli.get("horarios")
    return isinstance(horarios, dict) and len(horarios) > 0

def ordenar_fechas_ddmmyyyy(fechas):
    def parse_fecha(f):
        try:
            return datetime.strptime(f, "%d/%m/%Y")
        except ValueError:
            return datetime.max
    return sorted(fechas, key=parse_fecha)

def get_dias(peli):
    if tiene_fechas(peli):
        return ordenar_fechas_ddmmyyyy(list(peli["fechas"].keys()))
    elif tiene_horarios(peli):
        return ["Disponible"]
    return []

def get_idiomas(peli, dia, max_idiomas=3):
    if tiene_fechas(peli) and dia in peli["fechas"]:
        idiomas = list(peli["fechas"][dia].keys())
    elif tiene_horarios(peli):
        idiomas = list(peli["horarios"].keys())
    else:
        idiomas = []
    return sorted(idiomas)[:max_idiomas]

def get_horarios(peli, dia, idioma):
    if tiene_fechas(peli):
        return list(peli["fechas"].get(dia, {}).get(idioma, []))
    elif tiene_horarios(peli):
        return list(peli["horarios"].get(idioma, []))
    return []

def slugify(titulo):
    s = titulo.lower()
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("utf-8")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s

def seleccionar_entrada(peli, dia, idioma, hora):
    dias = get_dias(peli)
    if dia not in dias:
        raise ValueError("Día no disponible")
    idiomas = get_idiomas(peli, dia)
    if idioma not in idiomas:
        raise ValueError("Idioma no disponible para ese día")
    horas = get_horarios(peli, dia, idioma)
    if hora not in horas:
        raise ValueError("Horario no disponible para ese día/idioma")

    slug = peli.get("slug") or slugify(peli["titulo"])
    return {"slug": slug, "fecha": dia, "idioma": idioma, "hora": hora}



