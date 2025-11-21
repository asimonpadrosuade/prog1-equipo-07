from datetime import datetime, date
import unicodedata

def limpiar_texto(s: str) -> str:
    texto_sin_tilde = ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )
    return texto_sin_tilde.lower()

def duracion_en_minutos(d: str | None) -> int:
    d = d.lower().replace(" ", "")
    h, resto = d.split("h")
    m = resto.replace("m", "") or "0"
    return int(h) * 60 + int(m)
    

def horario_en_minutos(hora: str | None) -> int:
    h, m = hora.split(":") #A1
    minutos = int(h) * 60 + int(m)
    return minutos

def sacar_hora_horario(hora: str | None) -> int:
    h, m = hora.split(":")
    return int(h)

def dia_relativo(fecha: str) -> str:
    try:
        fecha = datetime.fromisoformat(fecha).date()
    except ValueError:
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

    hoy = date.today()
    diferencia = (fecha - hoy).days

    if diferencia == 0:
        return "Hoy"
    elif diferencia == 1:
        return "Mañana"
    else:
        return fecha.strftime("%d/%m/%Y")