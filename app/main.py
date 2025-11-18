import uvicorn
from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logica.utils import (
    buscar_peliculas,
    encontrar_peliculas,
    encontrar_funciones,
    obtener_funciones,
    peliculas
)
from app.logica.auth import comprobar_admin, verificar_usuario
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
def pelicula(request: Request, pelicula_id: int):
    pelicula = encontrar_peliculas(cargar_json("peliculas.json"), pelicula_id)
    funciones = encontrar_funciones(pelicula_id)
    precios = cargar_json("precios.json")

    fecha_selected = request.query_params.get("fecha")
    idioma_selected = request.query_params.get("idioma")
    hora_selected = request.query_params.get("hora")

    fechas, idiomas, horarios = obtener_funciones(funciones, fecha_selected, idioma_selected)

    return templates.TemplateResponse(
        "public/peliculas.html",
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


# Seleccion de asientos
@app.get("/asientos/{funcion_id}", response_class=HTMLResponse)


# Panel de admin
@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    if not comprobar_admin(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("admin/inicio.html", {"request": request})


@app.get("/admin/funcion", response_class=HTMLResponse)
def form_funcion(request: Request):
    if not comprobar_admin(request):
        return RedirectResponse("/login")
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
    if not comprobar_admin(request):
        return RedirectResponse("/login")
    agregar_funcion(pelicula_id, sala, fecha, hora, idioma)
    return RedirectResponse("/admin", status_code=302)

# Login y logout
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if comprobar_admin(request):
        return RedirectResponse("/admin")
    return templates.TemplateResponse("admin/login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if verificar_usuario(username, password):
        r = RedirectResponse("/admin", status_code=302)
        r.set_cookie("admin", "1")
        return r
    return RedirectResponse("/login", status_code=302)


@app.get("/logout")
def logout():
    r = RedirectResponse("/", status_code=302)
    r.delete_cookie("admin")
    return r

# Correr app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)