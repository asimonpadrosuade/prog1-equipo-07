# prog1-equipo-07
TP de Algoritmia y Estructura de Datos I

# 📌 Requisitos

Antes de instalar el proyecto, asegurate de tener instalado:
  Python 3.10 o superior
  pip (incluido con Python)
  
## 📁 Instalación del entorno

Crear el entorno virtual:
  python3 -m venv .venv

Activar el entorno:
En Linux / macOS:
  source .venv/bin/activate
  
En Windows:
  .\venv\Scripts\activate

Instalar dependencias:
  pip install --upgrade pip
  pip install -r requirements.txt

▶️ Ejecución del servidor
  uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

El proyecto quedará disponible en:
  http://127.0.0.1:8000