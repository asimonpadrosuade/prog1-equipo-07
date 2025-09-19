from datetime import datetime
import tkinter

ventana = tkinter.Tk()
ventana.geometry("1080x720")

titulo = tkinter.Label(ventana, text = "Bienvenido a PyTicket")
titulo.pack()

ventana.mainloop()

peliculas = {
    1: {"titulo": "El Conjuro 4", "fecha_lanzamiento": datetime(2025, 9, 5),  "categoría": "Terror", "idioma": "Subtitulada", "horarios": ["15:30", "18:00", "20:45"]},
    2: {"titulo": "Superman", "fecha_lanzamiento": datetime(2025, 7, 10), "categoría": "Accion", "idioma": "Castellano", "horarios": ["14:15", "17:00", "21:10"]},
    3: {"titulo": "Tron: Ares", "fecha_lanzamiento": datetime(2025, 10, 10), "categoría": "Accion", "idioma": "Subtitulada", "horarios": ["16:00", "19:30", "22:15"]},
    4: {"titulo": "Homo Argentum", "fecha_lanzamiento": datetime(2025, 8, 14), "categoría": "Comedia", "idioma": "Castellano", "horarios": ["13:50", "18:40", "20:10"]},
    5: {"titulo": "Mascotas al Rescate", "fecha_lanzamiento": datetime(2025, 8, 25), "categoría": "Animacion", "idioma": "Castellano", "horarios": ["12:30", "16:45", "19:00"]},
}

def formatear_moneda(valor):
    entero, dec = f"{valor:,.2f}".split(".")
    return f"$ {entero.replace(',', '.')},{dec}"

def precio_pelicula(edad, movistar):
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