from fastapi import APIRouter, Path
from Schemas.Usuario import UsuarioData
from controllers.usuarios_controller import *

usuarios = APIRouter(prefix="/usuarios",
                     tags=["Usuarios"],
                      responses={404: {"mensaje" : "No encontrado"}})

# URL-Usuarios funciones
# Recuperar todos los usuario registrados
@usuarios.get("/", status_code=200)
async def read_usuarios():
    return leer_usuarios_funcion() 
# Recuperar un respectivo usuario por la id
@usuarios.get("/{id:int}")
async def read_usuario(id: int = Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return leer_usuario_funcion(id)
# Ingresar un nuevo usuario
@usuarios.post("/ingresarUsuario/", status_code=201)
async def ingresar_usuario(user : UsuarioData):
    return ingresar_usuario_funcion(user)

# Actualizar un usuario por la id
@usuarios.put("/actualizarUsuario/{id}")
async def actualizar_usuario(user : UsuarioData,id : int =Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return actualizar_usuario_funcion(id , user)

# Eliminar un usuario por la id 
@usuarios.delete("/eliminarUsuario/{id}", status_code=204)
async def eliminar_usuario(id : int= Path(..., gt=0, description="El ID debe ser un entero mayor a cero")) :
    return eliminar_usuario_funcion(id)

