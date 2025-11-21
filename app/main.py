import uuid
import uvicorn
from fastapi import FastAPI, Request, Query, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logica.utils import (
    buscar_peliculas,
    calcular_total,
    cant_entradas,
    encontrar_peliculas,
    mostrar_funciones,
    obtener_funciones,
    agregar_funcion,
    encontrar_funciones_filtros,
    mostrar_asientos,
    crear_orden,
    encontrar_funciones,
)
from app.logica.json_access import cargar_json

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

reserva_temp = {}
asientos_temp = {}


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
    error: str | None = Query(None),
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
            "error": None,
        },
    )


@app.post("/pelicula/{pelicula_id}")
def recibir_entradas(
    request: Request,
    pelicula_id: int,
    comun: int = Form(0),
    menor: int = Form(0),
    jubilado: int = Form(0),
    fecha: str = Form(...),
    idioma: str = Form(...),
    hora: str = Form(...),
):
    total_entradas = cant_entradas(comun, menor, jubilado)
    if total_entradas == 0:
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
                "error": "Tenés que seleccionar al menos una entrada.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    reserva_id = str(uuid.uuid4())
    funcion_seleccionada = encontrar_funciones_filtros(pelicula_id, fecha, idioma, hora)
    total = calcular_total(comun, menor, jubilado)

    reserva_temp[reserva_id] = {
        "funcion_id": funcion_seleccionada[0]["id"],
        "entradas": {"comun": comun, "menor": menor, "jubilado": jubilado},
        "total": total,
        "cantidad_entradas": total_entradas,
        "confirmada": False,
    }
    return RedirectResponse(f"/asientos/{reserva_id}", status_code=303)


# Seleccion de asientos
@app.get("/asientos/{reserva_id}", response_class=HTMLResponse)
def asientos(request: Request, reserva_id: str, error: str | None = Query(None)):
    try:
        reserva = reserva_temp[reserva_id]
    except KeyError:
        return RedirectResponse("/", status_code=303)

    sala = mostrar_asientos(reserva["funcion_id"])
    return templates.TemplateResponse(
        "public/asientos.html",
        {
            "request": request,
            "reserva_id": reserva_id,
            "sala": sala,
            "total": reserva["cantidad_entradas"],
        },
    )


@app.post("/asientos")
def recibir_asientos(
    reserva_id: str = Form(...),
    asientos: list[str] = Form([]),
):
    reserva = reserva_temp.get(reserva_id)
    if not reserva:
        return RedirectResponse("/", status_code=303)
    max_sel = reserva["cantidad_entradas"]
    if len(asientos) != max_sel:
        return RedirectResponse(f"/asientos/{reserva_id}?error=cantidad", status_code=303)
    asientos_temp[reserva_id] = asientos
    return RedirectResponse(f"/resumen/{reserva_id}", status_code=303)


# Resumen
@app.get("/resumen/{reserva_id}", response_class=HTMLResponse)
def resumen(request: Request, reserva_id: str):
    try:
        reserva = reserva_temp[reserva_id]
        seleccion = asientos_temp[reserva_id]
        funcion = encontrar_funciones(reserva["funcion_id"])
    except KeyError:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "public/resumen.html",
        {"request": request, "orden": reserva, "asientos": seleccion, "funcion": funcion},
    )


@app.post("/resumen/{reserva_id}")
def confirmar_orden(
    reserva_id: str,
):
    reserva = reserva_temp.get(reserva_id)
    if not reserva:
        return RedirectResponse("/", status_code=303)

    asientos = asientos_temp.get(reserva_id)
    crear_orden(reserva, asientos)
    return RedirectResponse(f"/resumen/{reserva_id}?confirmada=1", status_code=303)


# Panel de admin
@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin/inicio.html", {"request": request})


# Crear Funciones
@app.get("/admin/funcion", response_class=HTMLResponse)
def mostrar_datos_funcion(request: Request):
    return templates.TemplateResponse(
        "admin/funcion.html",
        {
            "request": request,
            "peliculas": cargar_json("peliculas.json"),
            "salas": cargar_json("salas.json"),
        },
    )


@app.post("/admin/funcion")
def crear_funcion(
    pelicula_id: str = Form(...),
    sala: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(...),
    idioma: str = Form(...),
):
    agregar_funcion(pelicula_id, sala, fecha, hora, idioma)
    return RedirectResponse(url="/admin/funcion", status_code=303)


# Checkear ordenes temporales
@app.get("/debug/ordenes")
def debug_ordenes():
    return reserva_temp, asientos_temp


# Correr app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
