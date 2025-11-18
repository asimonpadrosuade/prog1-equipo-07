import uvicorn
from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logica.utils import (
    buscar_peliculas,
    encontrar_peliculas,
    cargar_funciones,
    guardar_funciones,
    cargar_salas,                         
    obtener_o_crear_butacas_por_funcion,  
    reservar_butaca_funcion,              
)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def busqueda(
    request: Request,
    q: str | None = Query(None),
    categoria: str | None = Query(None),
    duracion: str | None = Query(None),
):
    resultados = buscar_peliculas(q, categoria, duracion)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "peliculas": resultados,
            "busqueda": q,
            "categoria": categoria,
            "duracion": duracion,
        },
    )


@app.get("/pelicula/{pelicula_id}", response_class=HTMLResponse)
def pelicula(request: Request, pelicula_id: int):
    pelicula = encontrar_peliculas(pelicula_id)
    return templates.TemplateResponse(
        "peliculas.html", {"request": request, "pelicula": pelicula}
    )


@app.get("/asientos/{funcion_id}", response_class=HTMLResponse)
def asientos(request: Request, funcion_id: str):
    funciones = cargar_funciones()
    funcion = funciones.get(funcion_id)

    if not funcion:
        return RedirectResponse("/", status_code=302)

    salas = cargar_salas()
    butacas = obtener_o_crear_butacas_por_funcion(funcion, salas)
    guardar_funciones(funciones)

    return templates.TemplateResponse(
        "asientos.html",
        {
            "request": request,
            "funcion": funcion,
            "funcion_id": funcion_id,
            "butacas": butacas,
        },
    )


@app.post("/asientos/{funcion_id}/reservar")
async def reservar_asientos(
    request: Request, funcion_id: str, asientos: list[str] = Form(...)
):
    funciones = cargar_funciones()

    for asiento in asientos:
        fila, columna = map(int, asiento.split(","))
        resultado = reservar_butaca_funcion(funciones, funcion_id, fila, columna)
        # Podrías loguear resultado["msg"] si querés

    guardar_funciones(funciones)
    return RedirectResponse(f"/asientos/{funcion_id}", status_code=302)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
