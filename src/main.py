

# Funciones
def precio_pelicula(fecha_lanzamiento):
    precio_estandar = 7999
    precio_estreno = precio_estandar * 1.35
    hoy = datetime.now()
    dias_estreno = (hoy - fecha_lanzamiento).days
    return precio_estandar if dias_estreno >= 7 else precio_estreno

def seleccionar_pelicula(pid):
    peli = peliculas[pid]
    precio = precio_pelicula(peli["fecha_lanzamiento"])

# Diccionarios
peliculas = [
    {"titulo": "El Conjuro 4",
     "duracion": "2h 15m", 
     "categoria": "Terror",
     "idioma": {
         "Castellano": ("15:30", "18:00", "20:45", "23:15"),
         "Subtitulado": ("15:30", "18:00", "20:45")},
     "fecha_lanzamiento": datetime(2025, 9, 5),
     "imagen": "posters/el-conjuro-4.png"},

    {"titulo": "Superman",
     "duracion": "2h 9m",
     "categoria": "Acción",
     "idioma": {
         "Subtitulado": ("14:15", "17:00", "21:10")},
     "fecha_lanzamiento": datetime(2025, 7, 10),
     "imagen": ""},

    {"titulo": "Tron: Ares",
     "duracion": "1h 59m", 
     "categoria": "Accion",
     "idioma": {
         "Castellano": ("16:00", "22:15"),
         "Subtitulado": ("14:15", "17:00", "21:10")},
     "fecha_lanzamiento": datetime(2025, 10, 10),
     "imagen": ""},
    
    {"titulo": "Homo Argentum",
     "duracion": "1h 50m",
     "categoria": "Comedia",
     "idioma": {
         "Castellano": ("13:50", "18:40", "20:10")},
     "fecha_lanzamiento": datetime(2025, 8, 14),
     "imagen": ""},

    {"titulo": "Mascotas al Rescate",
     "duracion": "1h 39m",
     "categoria": "Animación",
     "idioma": {
         "Castellano": ("17:15", "19:30", "22:15"),
         "Subtitulado": ("12:30", "16:45")},
     "fecha_lanzamiento": datetime(2025, 8, 25),
     "imagen": ""}
]

# UI
ctk.set_appearance_mode("dark")
primary_bg = "#001427"

app = ctk.CTk()
app.geometry("1440x1440")
app.configure(fg_color=primary_bg)

title = ctk.CTkLabel(app, text="Bienvenido a PyTicket", font=("Arial", 24, "bold"), text_color="white")
title.pack(padx=24, pady=24)

frame_cartelera = ctk.CTkFrame(app, fg_color="transparent")
frame_cartelera.pack()

imagenes = {}

for pid, peli in enumerate(peliculas):
    ruta = peli.get("imagen") or ""

    if ruta:
        poster_img = Image.open(ruta)
    else:
        poster_img = Image.new("RGB", (320, 480), color=(15, 40, 60))

    poster = ctk.CTkImage(light_image=poster_img, dark_image=poster_img, size=(200, 300))
    imagenes[pid] = poster

    texto_btn = f"{peli['titulo']}\n{peli['duracion']} · {peli['categoria']}"
    btn = ctk.CTkButton(
        frame_cartelera,
        text=texto_btn,
        image=poster,
        compound="top",
        fg_color="transparent",
        text_color="white",
        font=("Arial", 18, "bold"),
        command=lambda pid=pid: seleccionar_pelicula(pid)
    )
    btn.pack(side="left", padx=10, pady=10)

app.mainloop()

filas = 5
columnas = 8
butacas = [[0 for _ in range(columnas)] for _ in range(filas)]


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
        print(f"Butaca ({f+1}, {c+1}) reservada ")
    else:
        print(f"Butaca ({f+1}, {c+1}) ocupada")


mostrar_sala()            # mostrar sala
reservar_butaca(0, 0)     # fila 0, columna 0
reservar_butaca(1, 4)     # fila 1, columna 4
reservar_butaca(1, 4)     # intentar reservar una ocupada
mostrar_sala()            

