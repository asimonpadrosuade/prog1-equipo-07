def formatear_moneda(valor):
    entero, dec = f"{valor:,.2f}".split(".")
    return f"$ {entero.replace(',', '.')},{dec}"

def precio_pelicula(edad, movistar):
    precio_estandar = 7999   
    precio_movistar = 7500   
    precio_reducido = 6999   
    if edad > 65:
        return "Jubilado", formatear_moneda(precio_reducido)
    elif edad < 6:
        return "Menor", formatear_moneda(precio_reducido)
    elif movistar == 1:
        return "Movistar", f´pullormatear_moneda(precio_movistar)

    else:
                return "Entrada", formatear_moneda(precio_estandar)