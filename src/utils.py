from datetime import datetime

#UI helpers
def mostrar_frame(frame):
    frame.pack(fill="both", expand=True)

def ocultar_frame(frame):
    frame.pack_forget()

def swap_frames(container, frame_nuevo):
    for child in container.winfo_children():
        child.pack_forget()
    frame_nuevo.pack(fill="both", expand=True)

#Precios
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

#Butacas
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
