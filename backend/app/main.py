from fastapi import FastAPI
from config.conexion import supabase  # Importar la sesión de la base de datos
from routers.usuarios import usuarios

# Inicializa la aplicación FastAPI
app = FastAPI()
#  Hacer que la aplicación incluya las rutas que vienen de usuarios
app.include_router(usuarios)



@app.get("/")
def read_usuarios():
    return {
        "hola" :"usuario1"
    }        