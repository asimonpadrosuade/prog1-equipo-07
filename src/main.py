from datetime import datetime
import tkinter
from PIL import Image, ImageTk

def precio_pelicula(fecha_lanzamiento):
  precio_estandar = 7999 #precio estandar
  precio_estreno = precio_estandar * 1.35 #35% mas caro por estreno
  hoy = datetime.now()
  dias_estreno = (hoy - fecha_lanzamiento).days
  return precio_estandar if dias_estreno>=7 else precio_estreno
  
def seleccionar_pelicula(pid):
   peli = peliculas[pid]
   precio = precio_pelicula(peli["fecha_lanzamiento"])

peliculas = {
    1: {"titulo": "El Conjuro 4", "fecha_lanzamiento": datetime(2025, 9, 5),  "categoría": "Terror", "idioma": "Subtitulada", "horarios": ["15:30", "18:00", "20:45"], "imagen": "posters/el-conjuro-4.png"},
    2: {"titulo": "Superman", "fecha_lanzamiento": datetime(2025, 7, 10), "categoría": "Accion", "idioma": "Castellano", "horarios": ["14:15", "17:00", "21:10"], "imagen": "superman-2025.png"},
    3: {"titulo": "Tron: Ares", "fecha_lanzamiento": datetime(2025, 10, 10), "categoría": "Accion", "idioma": "Subtitulada", "horarios": ["16:00", "19:30", "22:15"], "imagen": "tron-ares.png"},
    4: {"titulo": "Homo Argentum", "fecha_lanzamiento": datetime(2025, 8, 14), "categoría": "Comedia", "idioma": "Castellano", "horarios": ["13:50", "18:40", "20:10"], "imagen": "homo-argentum.png"},
    5: {"titulo": "Mascotas al Rescate", "fecha_lanzamiento": datetime(2025, 8, 25), "categoría": "Animacion", "idioma": "Castellano", "horarios": ["12:30", "16:45", "19:00"], "imagen": "mascotas-al-rescate.png"}
}

ventana = tkinter.Tk()
ventana.geometry("1080x720")

tkinter.Label(ventana, text = "Bienvenido a PyTicket", font=("Arial", 18)).pack(padx=15, pady=15)

frame_cartelera = tkinter.Frame(ventana)
frame_cartelera.pack()

imagenes = {}

for pid, peli in peliculas.items():
   if pid != 1: #porque solo se adjunto una imagen para la primera pelicula
        continue
   
   img = Image.open(peli["imagen"])
   img = img.resize((320, 480))
   foto = ImageTk.PhotoImage(img)

   imagenes[pid] = foto

   boton = tkinter.Button(
      frame_cartelera,
      text = peli["titulo"],
      image=foto,
      bg="lightgray",
      compound="top",
      command = lambda pid=pid: seleccionar_pelicula(pid)
      )
   boton.pack(padx=10, pady=10)

ventana.mainloop()