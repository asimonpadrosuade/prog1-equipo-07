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
    h, m = hora.split(":")
    minutos = int(h) * 60 + int(m)
    return minutos

def sacar_hora_horario(hora: str | None) -> int:
    h, m = hora.split(":")
    return int(h)