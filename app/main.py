import uuid
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logica.utils import (
    buscar_peliculas,
    encontrar_peliculas,
    mostrar_funciones,
    obtener_funciones,
    agregar_funcion,
    encontrar_funciones
)
from app.logica.json_access import cargar_json

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Pagina principal
@app.get("/", response_class=HTMLResponse)
def busqueda(
    request: Request,
    q: str | None = Query(None),
    categoria: str | None = Query(None),
    duracion: str | None = Query(None),
):
    resultados = buscar_peliculas(q, categoria, duracion)
    return templates.TemplateResponse(
        "public/inicio.html",
        {
            "request": request,
            "peliculas": resultados,
            "busqueda": q,
            "categoria": categoria,
            "duracion": duracion,
        },
    )


# Detalle de pelicula
@app.get("/pelicula/{pelicula_id}", response_class=HTMLResponse)
def pelicula(
    request: Request,
    pelicula_id: int,
    fecha: str | None = Query(None),
    idioma: str | None = Query(None),
    hora: str | None = Query(None),
):
    pelicula = encontrar_peliculas(cargar_json("peliculas.json"), pelicula_id)
    funciones = mostrar_funciones(pelicula_id)
    precios = cargar_json("precios.json")
    fechas, idiomas, horarios = obtener_funciones(funciones, fecha, idioma)
    return templates.TemplateResponse(
        "public/peliculas.html",
        {
            "request": request,
            "pelicula": pelicula,
            "funciones": funciones,
            "fechas": fechas,
            "idiomas": idiomas,
            "horarios": horarios,
            "fecha_selected": fecha,
            "idioma_selected": idioma,
            "hora_selected": hora,
            "precios": precios,
        },
    )

orden_temporal = {}
@app.post("/pelicula/{pelicula_id}")
def recibir_entradas(
    pelicula_id: int,
    comun: int = Form(0),
    menor: int = Form(0),
    jubilado: int = Form(0),
    fecha: str = Form(...),
    idioma: str = Form(...),
    hora: str = Form(...)
):
    compra_id = str(uuid.uuid4())
    funcion_seleccionada = encontrar_funciones(pelicula_id, fecha, idioma, hora)

    orden_temporal[compra_id] = {
        "funcion_id": funcion_seleccionada[0]["id"],
        "entradas": {
            "comun": comun,
            "menor": menor,
            "jubilado": jubilado,
        },
    }
    return RedirectResponse(url=f"/asientos?orden_id={compra_id}", status_code=303)


@app.get("/debug/ordenes")
def debug_ordenes():
    return orden_temporal

@app.get("/asientos", response_class=HTMLResponse)
def asientos(request: Request, orden_id: str = Query(...)):
    orden = orden_temporal.get(orden_id)
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    return templates.TemplateResponse("public/asientos.html", {"request": request, "orden": orden})


# Resumen de entradas previo a compra
@app.get("/resumen/{orden_id}", response_class=HTMLResponse)
def resumen(request: Request, orden_id: str):
    orden = orden_temporal.get(orden_id)
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    return templates.TemplateResponse(
        "public/resumen.html",
        {"request": request, "orden": orden},
    )

# Panel de admin
@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin/inicio.html", {"request": request})


@app.get("/admin/funcion", response_class=HTMLResponse)
def form_funcion(request: Request):
    return templates.TemplateResponse(
        "admin/funcion.html",
        {"request": request, "peliculas": cargar_json("peliculas.json"), "salas": cargar_json("salas.json")},
    )

@app.post("/admin/funcion")
def crear_funcion(
    request: Request,
    pelicula_id: str = Form(...),
    sala: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(...),
    idioma: str = Form(...),
):
    agregar_funcion(pelicula_id, sala, fecha, hora, idioma)

# Correr app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)