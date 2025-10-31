from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.data.peliculas import peliculas

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str | None = Query(None)):
  if q:
    resultados = [pelicula for pelicula in peliculas if q.lower() in pelicula['titulo'].lower()]
  else:
    resultados = peliculas

  return templates.TemplateResponse("index.html", {"request": request, "peliculas": resultados, "busqueda": q})