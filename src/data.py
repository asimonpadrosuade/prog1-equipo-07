from datetime import datetime

#Peliculas
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
        "imagen": "assets/posters/el-conjuro-4.png",
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
        "categoria": "Acción",
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
    {
        "titulo": "Una Batalla tras Otra",
        "duracion": "2h 10m",
        "categoria": "Acción",
        "fechas": {
            "15/11/2025": {"Castellano": ("15:00", "20:30")},
            "16/11/2025": {"Subtitulado": ("18:00", "22:15")},
        },
        "fecha_lanzamiento": datetime(2025, 9, 20),
        "imagen": "",
    },
    {
        "titulo": "Camina o Muere",
        "duracion": "1h 47m",
        "categoria": "Drama",
        "fechas": {
            "15/11/2025": {"Castellano": ("14:00", "19:30")},
            "16/11/2025": {"Subtitulado": ("16:15", "21:45")},
        },
        "fecha_lanzamiento": datetime(2025, 10, 2),
        "imagen": "",
    },
    {
        "titulo": "Jurassic World Renace",
        "duracion": "2h 25m",
        "categoria": "Aventura",
        "fechas": {
            "15/11/2025": {"Castellano": ("13:30", "18:00", "22:30")},
        },
        "fecha_lanzamiento": datetime(2025, 8, 30),
        "imagen": "",
    },
    {
        "titulo": "Lilo y Stich",
        "duracion": "1h 42m",
        "categoria": "Animación",
        "horarios": {
            "Castellano": ("12:30", "15:00", "18:00"),
            "Subtitulado": ("20:30",),
        },
        "fecha_lanzamiento": datetime(2025, 7, 25),
        "imagen": "",
    },
    {
        "titulo": "Avatar: el Camino del Agua",
        "duracion": "3h 12m",
        "categoria": "Ciencia Ficción",
        "fechas": {
            "15/11/2025": {
                "Castellano": ("15:00", "19:00"),
                "Subtitulado": ("21:30",),
            }
        },
        "fecha_lanzamiento": datetime(2025, 9, 10),
        "imagen": "",
    },
    {
        "titulo": "F1 la Película",
        "duracion": "1h 55m",
        "categoria": "Deporte",
        "fechas": {
            "15/11/2025": {"Castellano": ("16:00", "22:00")},
            "16/11/2025": {"Subtitulado": ("14:00", "20:00")},
        },
        "fecha_lanzamiento": datetime(2025, 10, 1),
        "imagen": "",
    },
    {
        "titulo": "Misión Imposible: Sentencia Final",
        "duracion": "2h 28m",
        "categoria": "Acción",
        "fechas": {
            "15/11/2025": {"Castellano": ("15:45", "20:15")},
            "16/11/2025": {"Subtitulado": ("18:30", "22:45")},
        },
        "fecha_lanzamiento": datetime(2025, 8, 5),
        "imagen": "",
    },
    {
        "titulo": "Los 4 Fantásticos: Primeros Pasos",
        "duracion": "2h 05m",
        "categoria": "Superhéroes",
        "fechas": {
            "15/11/2025": {"Castellano": ("14:30", "19:00")},
            "16/11/2025": {"Subtitulado": ("17:00", "21:30")},
        },
        "fecha_lanzamiento": datetime(2025, 9, 15),
        "imagen": "",
    },
]

#Butacas
filas = 5
columnas = 8
butacas = [[0 for _ in range(columnas)] for _ in range(filas)]

#Layout
max_columns = 5
poster_unit = 120
poster_size = (2 * poster_unit, 3 * poster_unit)

#Tipografia
text_size = 18
title_size = 32
font_family = "Montserrat"