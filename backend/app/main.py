from fastapi import FastAPI
from config.conexion import supabase  # Importar la sesión de la base de datos
from routers.usuarios import usuarios
from fastapi.middleware.cors import CORSMiddleware
from routers.productos import productos
from routers import auth
from routers.Comentario import comentario
from routers.carrito import carrito
from routers.inventario import inventario


# Inicializa la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5173",  # La URL de tu frontend en desarrollo
    # Puedes agregar otras URLs aquí, como la URL de producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite solicitudes desde estos orígenes
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Permite todos los encabezados
)
#Hacer que la aplicación incluya las rutas que vienen de usuarios

app.include_router(usuarios)
app.include_router(productos)
app.include_router(auth.auth_router)
app.include_router(comentario)
app.include_router(carrito)
app.include_router(inventario)
@app.get("/")

def read_usuarios():
    return {
        "hola" :"usuario2"
    }        
