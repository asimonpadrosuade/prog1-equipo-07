import customtkinter as ctk
from PIL import Image
from .font import load_fonts
from .data import peliculas, poster_size, max_columns
from .utils import ocultar_frame, mostrar_frame

imagenes = {}


# Crea la imagen para el poster importandola o colocando un placeholder
def crear_poster(path):
    try:
        poster_img = Image.open(path) if path else None
    except (FileNotFoundError, OSError):
        poster_img = None

    if poster_img is None:
        # Fallback placeholder
        poster_img = Image.new(
            "RGB", (poster_size[0], poster_size[1]), color=(15, 40, 60)
        )

    return ctk.CTkImage(
        light_image=poster_img,
        dark_image=poster_img,
        size=poster_size,
    )


def seleccion_peliculas(app):
    global contenedor_main

    text_bold, _, title_bold = load_fonts(app)

    contenedor_main = ctk.CTkFrame(app, fg_color="transparent")
    contenedor_main.pack(fill="both", expand=True, padx=40, pady=40)

    titulo_principal = ctk.CTkLabel(
        contenedor_main,
        text="Bienvenido a PyTicket",
        font=title_bold,
        text_color="white",
    )
    titulo_principal.pack(pady=(0, 30))

    contenedor_peliculas = ctk.CTkScrollableFrame(
        contenedor_main,
        fg_color="transparent",
        orientation="vertical",
    )
    contenedor_peliculas.pack(fill="both", expand=True)

    for col in range(max_columns):
        contenedor_peliculas.grid_columnconfigure(col, weight=1, uniform="cols")

    for poster_id, pelicula in enumerate(peliculas):
        image_path = pelicula.get("imagen") or ""
        poster_image = crear_poster(image_path)
        imagenes[poster_id] = poster_image

        titulo = pelicula.get("titulo", "")
        duracion = pelicula.get("duracion", "")
        categoria = pelicula.get("categoria", "")
        datos_pelicula = f"{titulo}\n{duracion} · {categoria}"

        row_index, col_index = divmod(poster_id, max_columns)

        btn_pelicula = ctk.CTkButton(
            contenedor_peliculas,
            text=datos_pelicula,
            image=poster_image,
            compound="top",
            fg_color="transparent",
            text_color="white",
            font=text_bold,
            width=poster_size[0],
            command=lambda peli=pelicula: (
                ocultar_frame(contenedor_peliculas),
                titulo_principal.configure(
                    text=f"Confirma tu seleccion de pelicula: {peli['titulo']}"
                ),
            ),
        )

        btn_pelicula.image = poster_image
        btn_pelicula.grid(row=row_index, column=col_index, sticky="n", padx=8, pady=12)

    container_entradas = ctk.CTkFrame(app)
    titulo_entradas = ctk.CTkLabel(
        container_entradas, text="Selecciona tus entradas", font=title_bold
    )
    titulo_entradas.pack(pady=20)
