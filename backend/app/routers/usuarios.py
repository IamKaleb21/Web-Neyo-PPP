from fastapi import APIRouter
from Schemas.Usuario import UsuarioData
from controllers.usuarios_controller import *

usuarios = APIRouter(prefix="/usuarios",
                     tags=["Usuarios"],
                      responses={404: {"mensaje" : "No encontrado"}})

# URL-Usuarios funciones
@usuarios.get("/")
def read_usuarios():
    return leer_usuarios_funcion() 

@usuarios.get("/{id:int}")
def read_usuario(id: int):
    return leer_usuario_funcion(id)

@usuarios.post("/ingresarUsuario/")
def ingresar_usuario(user : UsuarioData):
    return ingresar_usuario_funcion(user)


@usuarios.put("/actualizarUsuario/{id}")
def actualizar_usuario(id : int , user : UsuarioData):
    return actualizar_usuario_funcion(id , user)


@usuarios.delete("/eliminarUsuario/{id}")
def eliminar_usuario(id : int) :
    return eliminar_usuario_funcion(id)

