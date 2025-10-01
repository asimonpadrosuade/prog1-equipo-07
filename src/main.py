from datetime import datetime
import customtkinter as ctk
from PIL import Image


# Funciones
def precio_pelicula(fecha_lanzamiento):
    precio_estandar = 7999
    precio_estreno = precio_estandar * 1.35
    hoy = datetime.now()
    dias_estreno = (hoy - fecha_lanzamiento).days
    return precio_estandar if dias_estreno >= 7 else precio_estreno


def mostrar_sala():
    print("Sala:")
    for fila in butacas:
        for asiento in fila:
            if asiento == 0:
                print("O", end=" ")
            else:
                print("X", end=" ")
        print()
    print()


def reservar_butaca(f, c):
    if butacas[f][c] == 0:
        butacas[f][c] = 1
        print(f"Butaca ({f + 1}, {c + 1}) reservada ")
    else:
        print(f"Butaca ({f + 1}, {c + 1}) ocupada")


def mostrar_entradas():
    container_entradas.pack(fill="both")

def ir_a_pelicula(peli):
    contenedor_main.pack_forget()
    titulo_entradas.configure(text=f"Selecciona tus entradas para {peli['titulo']}")
    container_entradas.pack(fill="both", expand=True)

# Definir cantiad de filas y butacas
filas = 5
columnas = 8
butacas = [[0 for _ in range(columnas)] for _ in range(filas)]

# Diccionario de peliculas
peliculas = [
    {
        "titulo": "El Conjuro 4",
        "duracion": "2h 15m",
        "categoria": "Terror",
        "fechas": {
            "15/11/2025": {
                "Castellano": ("15:30", "18:00", "20:45", "23:15"),
                "Subtitulado": ("15:30", "18:00", "20:45"),
            },
            "16/11/2025": {
                "Castellano": ("14:30", "18:00", "20:45", "23:15"),
                "Subtitulado": ("15:30", "17:00", "19:45"),
            },
        },
        "fecha_lanzamiento": datetime(2025, 9, 5),
        "imagen": "posters/el-conjuro-4.png",
    },
    {
        "titulo": "Superman",
        "duracion": "2h 9m",
        "categoria": "Acción",
        "fechas": {
            "15/11/2025": {"Subtitulado": ("14:15", "17:00", "21:10")},
            "16/11/2025": {"Subtitulado": ("13:15", "16:00", "20:10")},
        },
        "fecha_lanzamiento": datetime(2025, 7, 10),
        "imagen": "",
    },
    {
        "titulo": "Tron: Ares",
        "duracion": "1h 59m",
        "categoria": "Accion",
        "fechas": {
            "15/11/2025": {
                "Castellano": ("16:00", "22:15"),
                "Subtitulado": ("14:15", "17:00", "21:10"),
            }
        },
        "fecha_lanzamiento": datetime(2025, 10, 10),
        "imagen": "",
    },
    {
        "titulo": "Homo Argentum",
        "duracion": "1h 50m",
        "categoria": "Comedia",
        "horarios": {"Castellano": ("13:50", "18:40", "20:10")},
        "fecha_lanzamiento": datetime(2025, 8, 14),
        "imagen": "",
    },
    {
        "titulo": "Mascotas al Rescate",
        "duracion": "1h 39m",
        "categoria": "Animación",
        "horarios": {
            "Castellano": ("17:15", "19:30", "22:15"),
            "Subtitulado": ("12:30", "16:45"),
        },
        "fecha_lanzamiento": datetime(2025, 8, 25),
        "imagen": "",
    },
]

# UI
ctk.set_appearance_mode("dark")
primary_bg = "#001427"

app = ctk.CTk()
app.geometry("1440x1440")
app.configure(fg_color=primary_bg)

contenedor_main = ctk.CTkFrame(app, fg_color="transparent")
contenedor_main.pack(padx=60, pady=60)

titulo_principal = ctk.CTkLabel(
    contenedor_main,
    text="Bienvenido a PyTicket",
    font=("Arial", 28, "bold"),
    text_color="white",
)
titulo_principal.pack(pady=(0, 30))

poster_pelicula = ctk.CTkFrame(contenedor_main, fg_color="transparent")
poster_pelicula.pack(fill="x", expand=True)
poster_pelicula.grid_columnconfigure((0,1,2,3), weight=1)

container_entradas = ctk.CTkFrame(app)

titulo_entradas = ctk.CTkLabel(
    container_entradas,
    text=f"Selecciona tus entradas para {2}",
    font=("Arial", 18),
)
titulo_entradas.pack()

imagenes = {}

# Generar los posters para todas las peliculas disponibles
max_cols = 5
for col in range(max_cols):
    poster_pelicula.grid_columnconfigure(col, weight=1)
for pid, peli in enumerate(peliculas):
    ruta = peli.get("imagen") or ""

    if ruta:
        poster_img = Image.open(ruta)
    else:
        poster_img = Image.new("RGB", (320, 480), color=(15, 40, 60))

    poster = ctk.CTkImage(
        light_image=poster_img, dark_image=poster_img, size=(200, 300)
    )
    imagenes[pid] = poster

    datos_pelicula = f"{peli['titulo']}\n{peli['duracion']} · {peli['categoria']}"  # Llamamos a las llaves del diccionario

    r = pid // max_cols
    c = pid % max_cols

    btn_pelicula = ctk.CTkButton(
        poster_pelicula,
        text=datos_pelicula,
        image=poster,
        compound="top",
        fg_color="transparent",
        text_color="white",
        font=("Arial", 18, "bold"),
    )
    btn_pelicula.grid(row=r, column=c, sticky="ew", padx=4, pady=10)

app.mainloop()
