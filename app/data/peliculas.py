from datetime import datetime

#Peliculas
peliculas = [
    {
        "id": 1,
        "titulo": "El Conjuro 4",
        "duracion": "2h 15m",
        "categoria": "Terror",
        "Sinopsis": "Ed y Lorraine Warren vuelven para enfrentar un caso definitivo: la familia Smurl afirma estar siendo atacada por entidades malignas en su hogar, luego de que un espejo antiguo y perturbador reaparezca como regalo. Mientras los Warrens intentan ayudar, se ven inmersos en fuerzas sobrenaturales que los desafían a nivel personal, obligándolos a confrontar secretos de su pasado y el límite entre lo humano y lo paranormal.",
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
        "poster": "/static/posters/el-conjuro-4.png",
    },
    {
        "id": 2,
        "titulo": "Superman",
        "duracion": "2h 9m",
        "categoria": "Acción",
        "Sinopsis": "Clark Kent / Superman debe hallar un equilibrio entre sus raíces kriptonianas y su crianza humana, mientras actúa como símbolo de esperanza en un mundo cínico. En esta reinvención dirigida por James Gunn, el héroe no es sólo fuerza y poderes, sino también compasión y convicción de que la bondad aún tiene lugar en la humanidad.",
        "fechas": {
            "15/11/2025": {"Subtitulado": ("14:15", "17:00", "21:10")},
            "16/11/2025": {"Subtitulado": ("13:15", "16:00", "20:10")},
        },
        "fecha_lanzamiento": datetime(2025, 7, 10),
        "poster": "/static/posters/superman.webp",
    },
    {
        "id": 3,
        "titulo": "Tron: Ares",
        "duracion": "1h 59m",
        "categoria": "Acción",
        "Sinopsis": "Ares, un programa de avanzada del mundo digital, es enviado al mundo real para cumplir una misión peligrosa: representa el primer puente directo entre la humanidad y seres creados por inteligencia artificial. En un conflicto que trasciende fronteras tecnológicas, humanos e IA chocan en una trama de poder, identidad y desafío.",
        "fechas": {
            "15/11/2025": {
                "Castellano": ("16:00", "22:15"),
                "Subtitulado": ("14:15", "17:00", "21:10"),
            }
        },
        "fecha_lanzamiento": datetime(2025, 10, 10),
        "poster": "/static/posters/tron-ares.jpg",
    },
    {
        "id": 4,
        "titulo": "Homo Argentum",
        "duracion": "1h 50m",
        "categoria": "Comedia",
        "Sinopsis":"Una antológica comedia argentina compuesta por 16 historias independientes, todas protagonizadas por Guillermo Francella en distintos roles. Cada relato aborda con humor, ironía y mirada crítica la cultura, las costumbres y las tensiones sociales del “ser argentino”, ofreciendo un espejo de identidad nacional que provoca risas... y reflexión.",
        "horarios": {"Castellano": ("13:50", "18:40", "20:10")},
        "fecha_lanzamiento": datetime(2025, 8, 14),
        "poster": "/static/posters/Homo-argentum.webp",
    },
    {
        "id": 5,
        "titulo": "Mascotas al Rescate",
        "duracion": "1h 39m",
        "categoria": "Animación",
        "Sinopsis":"Cuando un tren lleno de mascotas arranca inesperadamente sin humanos a bordo, los animales descubren que Hans, un tejón vengativo, está detrás de todo. Con el choque inminente, Falcon —un mapache audaz— lidera una misión desesperada para salvarlos a todos.",
        "horarios": {
            "Castellano": ("17:15", "19:30", "22:15"),
            "Subtitulado": ("12:30", "16:45"),
        },
        "fecha_lanzamiento": datetime(2025, 8, 25),
        "poster": "/static/posters/mascotas-al-rescate.jpg",
    },
    {
        "id": 6,
        "titulo": "Una Batalla tras Otra",
        "duracion": "2h 10m",
        "categoria": "Acción",
        "Sinopsis": "El revolucionario fracasado Bob (DiCaprio) vive en un estado de paranoia por culpa de los efectos de las drogas, sobreviviendo de forma aislada con su enérgica e independiente hija, Willa (Infiniti). Cuando su malvado némesis (Penn) reaparece después de 16 años y su hija desaparece, el ex radical lucha por encontrarla, padre e hija lucharan contra las consecuencias de su pasado.",
        "fechas": {
            "15/11/2025": {"Castellano": ("15:00", "20:30")},
            "16/11/2025": {"Subtitulado": ("18:00", "22:15")},
        },
        "fecha_lanzamiento": datetime(2025, 9, 20),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "id": 7,
        "titulo": "Camina o Muere",
        "duracion": "1h 47m",
        "categoria": "Drama",
        "Sinopsis":"De la esperada adaptación de la primera novela del maestro del suspenso Stephen King, y bajo la dirección de Francis Lawrence, llega CAMINA O MUERE: un thriller intenso, estremecedor y profundamente emocional. Una historia que pone a prueba no solo los límites de sus protagonistas, sino también los del espectador, con una pregunta inquietante: ¿Hasta dónde serías capaz de llegar? Cien adolescentes son obligados a caminar sin detenerse. Si se detienen, mueren. Solo uno podrá sobrevivir.",
        "fechas": {
            "15/11/2025": {"Castellano": ("14:00", "19:30")},
            "16/11/2025": {"Subtitulado": ("16:15", "21:45")},
        },
        "fecha_lanzamiento": datetime(2025, 10, 2),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "titulo": "Jurassic World Renace",
        "duracion": "2h 25m",
        "categoria": "Aventura",
        "Sinopsis":"Cinco años después de Jurassic World Dominion, los dinosaurios restantes habitan zonas ecuatoriales con climas similares a los antiguos. Tres criaturas colosales tienen en su ADN la clave para un fármaco revolucionario. Un equipo conformado por operativos especiales, científicos y aventureros debe adentrarse en una isla secreta para extraer esas muestras, enfrentando peligros, traiciones y criaturas imposibles.",
        "fechas": {
            "15/11/2025": {"Castellano": ("13:30", "18:00", "22:30")},
        },
        "fecha_lanzamiento": datetime(2025, 8, 30),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "titulo": "Lilo y Stich",
        "duracion": "1h 42m",
        "categoria": "Animación",
        "Sinopsis":"La nueva versión de acción real del clásico animado de Disney de 2002, LILO Y STITCH es la conmovedora y divertidísima historia de una niña hawaiana y el alienígena fugitivo que la ayuda a reconstruir su familia.",
        "horarios": {
            "Castellano": ("12:30", "15:00", "18:00"),
            "Subtitulado": ("20:30",),
        },
        "fecha_lanzamiento": datetime(2025, 7, 25),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "titulo": "Avatar: el Camino del Agua",
        "duracion": "3h 12m",
        "categoria": "Ciencia Ficción",
        "Sinopsis":"Jake Sully y Neytiri tienen familia en Pandora, pero una amenaza del pasado los obliga a abandonar su hogar submarino. Para sobrevivir, deben enfrentarse a los elementos del agua, pactar con clanes submarinos y encontrar dónde pertenece su linaje en el nuevo mundo.",
        "fechas": {
            "15/11/2025": {
                "Castellano": ("15:00", "19:00"),
                "Subtitulado": ("21:30",),
            }
        },
        "fecha_lanzamiento": datetime(2025, 9, 10),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "titulo": "F1 la Película",
        "duracion": "1h 55m",
        "categoria": "Deporte",
        "Sinopsis":"La adrenalina de la Fórmula 1 llevada al cine: pilotos, velocidad extrema, rivalidades, sacrificios y el brillo de las máquinas más avanzadas. Una mirada humana detrás del casco y la pasión que mueve a un deporte que exige perfección en cada curva.",
        "fechas": {
            "15/11/2025": {"Castellano": ("16:00", "22:00")},
            "16/11/2025": {"Subtitulado": ("14:00", "20:00")},
        },
        "fecha_lanzamiento": datetime(2025, 10, 1),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "titulo": "Misión Imposible: Sentencia Final",
        "duracion": "2h 28m",
        "categoria": "Acción",
        "Sinopsis":"Ethan Hunt y el equipo IMF enfrentan su misión más peligrosa: una conspiración global que pondrá en jaque no sólo su lealtad, sino la seguridad del mundo. Cada paso es decisivo, cada error mortal.",
        "fechas": {
            "15/11/2025": {"Castellano": ("15:45", "20:15")},
            "16/11/2025": {"Subtitulado": ("18:30", "22:45")},
        },
        "fecha_lanzamiento": datetime(2025, 8, 5),
        "poster": "/static/posters/placeholder.png",
    },
    {
        "titulo": "Los 4 Fantásticos: Primeros Pasos",
        "duracion": "2h 05m",
        "categoria": "Superhéroes",
        "Sinopsis":"Cuatro jóvenes científicos sufren un accidente dimensional que les otorga poderes extraordinarios. Mientras aprenden a controlarlos, deben balancear sus vidas normales con la responsabilidad de proteger al mundo de amenazas cósmicas desconocidas.",
        "fechas": {
            "15/11/2025": {"Castellano": ("14:30", "19:00")},
            "16/11/2025": {"Subtitulado": ("17:00", "21:30")},
        },
        "fecha_lanzamiento": datetime(2025, 9, 15),
        "poster": "/static/posters/placeholder.png",
    },
]