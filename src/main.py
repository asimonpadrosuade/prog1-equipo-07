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
