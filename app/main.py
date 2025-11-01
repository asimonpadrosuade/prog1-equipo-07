import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logica.funciones import buscar_peliculas, encontrar_peliculas

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
def mostrar_pelicula(request: Request, pelicula_id: int):
    pelicula = encontrar_peliculas(pelicula_id)
    return templates.TemplateResponse(
        "peliculas.html", {"request": request, "pelicula": pelicula}
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
