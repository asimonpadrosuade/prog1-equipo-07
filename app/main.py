import uvicorn
from fastapi import FastAPI,Request,Query,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logica.funciones import buscar_peliculas,encontrar_peliculas,PRECIOS,infer_formatos,fechas_disponibles,idiomas_para,horarios_para

app=FastAPI()
templates=Jinja2Templates(directory="app/templates")
app.mount("/static",StaticFiles(directory="app/static"),name="static")

@app.get("/",response_class=HTMLResponse)
def busqueda(request:Request,q:str|None=Query(None),categoria:str|None=Query(None),duracion:str|None=Query(None)):
    resultados=buscar_peliculas(q,categoria,duracion)
    return templates.TemplateResponse("index.html",{
        "request":request,
        "peliculas":resultados,
        "busqueda":q,
        "categoria":categoria,
        "duracion":duracion
    })

@app.get("/pelicula/{pelicula_id}",response_class=HTMLResponse)
def mostrar_pelicula(request:Request,pelicula_id:int):
    pelicula=encontrar_peliculas(pelicula_id)
    formatos=infer_formatos(pelicula)
    fechas=fechas_disponibles(pelicula)
    fecha_sel=fechas[0] if fechas else None
    idiomas=idiomas_para(pelicula,fecha_sel)
    idioma_sel=idiomas[0] if idiomas else None
    horarios=horarios_para(pelicula,fecha_sel,idioma_sel) if idioma_sel else []
    return templates.TemplateResponse("peliculas.html",{
        "request":request,
        "pelicula":pelicula,
        "formatos":formatos,
        "fecha_sel":fecha_sel,
        "fechas":fechas,
        "idioma_sel":idioma_sel,
        "idiomas":idiomas,
        "horarios":horarios,
        "precios":PRECIOS,
        "seleccion_confirmada":False
    })

@app.post("/pelicula/{pelicula_id}",response_class=HTMLResponse)
def confirmar_seleccion(request:Request,pelicula_id:int,formato:str=Form(...),fecha:str|None=Form(None),idioma:str=Form(...),horario:str=Form(...)):
    pelicula=encontrar_peliculas(pelicula_id)
    formatos=infer_formatos(pelicula)
    fechas=fechas_disponibles(pelicula)
    idiomas=idiomas_para(pelicula,fecha)
    horarios=horarios_para(pelicula,fecha,idioma)
    seleccion={"formato":formato,"fecha":fecha,"idioma":idioma,"horario":horario}
    return templates.TemplateResponse("peliculas.html",{
        "request":request,
        "pelicula":pelicula,
        "formatos":formatos,
        "fecha_sel":fecha,
        "fechas":fechas,
        "idioma_sel":idioma,
        "idiomas":idiomas,
        "horarios":horarios,
        "precios":PRECIOS,
        "seleccion_confirmada":True,
        "seleccion":seleccion
    })

if __name__=="__main__":
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
