import customtkinter as ctk
from . import state
from .font import load_font
from .ui import seleccion_peliculas

state.app = ctk.CTk()
state.app.configure(fg_color="#001427")
state.app.geometry("1440x1440")

state.FONTS["text_bold"]  = load_font(state.app, size=16)
state.FONTS["title_bold"] = load_font(state.app, size=22)

state.container_principal = ctk.CTkFrame(state.app, fg_color="transparent")
state.container_principal.pack(fill="both", expand=True)

seleccion_peliculas(state.app)
state.app.mainloop()