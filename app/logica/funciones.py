from datetime import datetime, timedelta
from app.data.peliculas import peliculas

#Precios
PRECIOS={"comun":15000,"menor_jubilado":10000,"movistar":12000}

def get_pelicula(peliculas,pid):
    for p in peliculas:
        if p["id"]==pid:return p
    return None

def infer_formatos(p):
    return p.get("formatos",["2D"])

def fechas_disponibles(p):
    if "fechas"in p and isinstance(p["fechas"],dict):
        try:return sorted(p["fechas"].keys(),key=lambda d:datetime.strptime(d,"%d/%m/%Y"))
        except:return list(p["fechas"].keys())
    if "horarios"in p:
        hoy=datetime.today()
        return [(hoy+timedelta(days=i)).strftime("%d/%m/%Y") for i in range(3)]
    return [None]

def idiomas_para(p,fecha):
    if fecha and "fechas"in p:return list(p["fechas"][fecha].keys())
    if "horarios"in p:return list(p["horarios"].keys())
    return []

def horarios_para(p,fecha,idioma):
    if fecha and "fechas"in p:return list(p["fechas"][fecha].get(idioma,()))
    if "horarios"in p:return list(p["horarios"].get(idioma,()))
    return []

def encontrar_peliculas(pid:int):
    return get_pelicula(peliculas,pid)

def buscar_peliculas(q=None,categoria=None,duracion=None):
    res=peliculas
    if q:
        ql=q.lower()
        res=[p for p in res if ql in p["titulo"].lower()]
    if categoria:
        def match_cat(p):
            c=p.get("categoria")
            if isinstance(c,set):return categoria in c or categoria.lower() in {x.lower() for x in c}
            if isinstance(c,str):return categoria.lower() in c.lower()
            return False
        res=[p for p in res if match_cat(p)]
    return res

#Butacas
def mostrar_sala(butacas):
    print("Sala:")
    for fila in butacas:
        for asiento in fila:
            print("O" if asiento==0 else "X",end=" ")
        print()
    print()

def reservar_butaca(butacas,f,c):
    if butacas[f][c]==0:
        butacas[f][c]=1
        print(f"Butaca ({f+1}, {c+1}) reservada ")
    else:
        print(f"Butaca ({f+1}, {c+1}) ocupada")

filas=5
columnas=8
butacas=[[0 for _ in range(columnas)] for _ in range(filas)]
