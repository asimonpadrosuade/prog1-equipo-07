from pathlib import Path
from functools import lru_cache
import json

# Acceder
peliculas_ruta = Path("app/data/peliculas.json")
usuarios_ruta = Path("app/data/usuarios.json")
funciones_ruta = Path("app/data/funciones.json")
salas_ruta = Path("app/data/salas.json")

# Cargar
@lru_cache()
def cargar_peliculas():
    with peliculas_ruta.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache()
def cargar_usuarios():
    with usuarios_ruta.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache()
def cargar_funciones():
    with funciones_ruta.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache()
def cargar_salas():
    with salas_ruta.open(encoding="utf-8") as f:
        return json.load(f)

# Guardar
def guardar_funciones(funciones):
    with funciones_ruta.open("w", encoding="utf-8") as f:
        json.dump(funciones, f, ensure_ascii=False, indent=2)
    cargar_funciones.cache_clear()