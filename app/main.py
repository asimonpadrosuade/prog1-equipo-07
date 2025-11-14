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
    encontrar_funciones,
    verificar_usuario,
    agregar_funcion,
    obtener_funciones,
    peliculas
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


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if request.cookies.get("admin") == "1":
        return RedirectResponse("/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if verificar_usuario(username, password):
        response = RedirectResponse("/admin", status_code=302)
        response.set_cookie("admin", "1")
        return response
    return RedirectResponse("/login", status_code=302)


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    if request.cookies.get("admin") != "1":
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post("/admin/funcion")
def funcion(
    request: Request,
    pelicula_id: str = Form(...),
    sala: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(...),
    idioma: str = Form(...),
):
    if request.cookies.get("admin") != "1":
        return RedirectResponse("/login", status_code=302)
    agregar_funcion(pelicula_id, sala, fecha, hora, idioma)
    return RedirectResponse("/admin", status_code=302)


@app.get("/admin/funcion", response_class=HTMLResponse)
def mostrar_funciones(request: Request):
    if request.cookies.get("admin") != "1":
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse(
        "funcion.html", {"request": request, "peliculas": peliculas}
    )


@app.get("/pelicula/{pelicula_id}", response_class=HTMLResponse)
def pelicula(request: Request, pelicula_id: int):
    pelicula = encontrar_peliculas(pelicula_id)
    funciones = encontrar_funciones(pelicula_id)
    fecha_selected = request.query_params.get("fecha")
    idioma_selected = request.query_params.get("idioma")
    fechas, idiomas, horarios = obtener_funciones(
        funciones, fecha_selected, idioma_selected
    )
    return templates.TemplateResponse(
        "peliculas.html",
        {
            "request": request,
            "pelicula": pelicula,
            "funciones": funciones,
            "fechas": fechas,
            "idiomas": idiomas,
            "horarios": horarios,
            "fecha_selected": fecha_selected,
            "idioma_selected": idioma_selected,
        },
    )


@app.get("/asientos/{funcion_id}", response_class=HTMLResponse)
def asientos(request: Request, funcion_id: str):
    funciones = cargar_funciones()
    funcion = funciones.get(funcion_id)
    return templates.TemplateResponse(
        "asientos.html",
        {"request": request, "funcion": funcion, "funcion_id": funcion_id},
    )


@app.post("/asientos/{funcion_id}/reservar")
async def reservar_asientos(
    request: Request, funcion_id: str, asientos: list[str] = Form(...)
):
    funciones = cargar_funciones()
    funcion = funciones.get(funcion_id)
    if not funcion:
        return RedirectResponse("/", status_code=302)
    for asiento in asientos:
        fila, columna = map(int, asiento.split(","))
        funcion["asientos"][fila][columna] = 1
    guardar_funciones(funciones)
    return RedirectResponse(f"/asientos/{funcion_id}", status_code=302)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
