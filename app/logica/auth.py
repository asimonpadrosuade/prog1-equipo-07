from app.logica.json_access import cargar_usuarios

def comprobar_admin(request):
    return request.cookies.get("admin") == "1"


def verificar_usuario(username, password):
    usuarios = cargar_usuarios()
    data = usuarios.get(username)
    if not data:
        return False
    hashed = data["password"]
    import bcrypt

    return bcrypt.checkpw(password.encode(), hashed.encode())