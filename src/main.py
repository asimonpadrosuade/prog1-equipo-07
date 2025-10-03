<<<<<<< HEAD
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
        return "Movistar", f´pullormatear_moneda(precio_movistar)

    else:
                return "Entrada", formatear_moneda(precio_estandar)
=======
import customtkinter as ctk
from .ui import seleccion_peliculas
from .font import load_font
from .data import text_size, title_size

def main():
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.geometry("1440x1440")
    app.configure(fg_color="#001427")
    app.title("PyTicket")
    text_bold = load_font(app, text_size)
    title_bold = load_font(app, title_size)

    seleccion_peliculas(app, text_bold, title_bold)

    app.mainloop()

if __name__ == "__main__":
    main()
>>>>>>> 942fcb8a1e0543ec5049b7f68a8aa33cc3209b05
