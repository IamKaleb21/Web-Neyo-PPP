from fastapi import APIRouter
from Schemas.Comentario import ComentarioData
from controllers.Comentario_controller import *

comentario = APIRouter(prefix="/comentario",
                     tags=["Comentario"],
                      responses={404: {"mensaje" : "No encontrado"}})


# URL -Comentario funciones
@comentario.post("/crearComentario")
def crear_comentario(comentario: ComentarioData):
    return crear_cometario_controller(comentario)

# Recuperar comentarios de un respectivo producto
@comentario.get("/RecuperarProducto/{idProducto:int}")
def mostrar_comentario_producto(idProducto: int):
    return mostrar_comentarios_producto_controller(idProducto)

# Recuperar comentarios de un respectivo cliente
@comentario.get("/RecuperarCliente/{idCliente:int}")
def mostrar_comentario_cliente(idCliente: int):
    return mostrar_comentarios_cliente_controller(idCliente)

# Eliminar un comentario
@comentario.delete("/Eliminar/{idComentario: int}")
def eliminar_comentario(idComentario: int):
    return eliminar_comentario_controller(idComentario)

# Eliminar todos los comentarios de un usuario
@comentario.delete("/EliminarTodo/{idCliente: int}")
def eliminar_comentarios_cliente(idCliente: int):
    return eliminar_comentarios_controller_cliente(idCliente)
# Actualizar comentario
@comentario.put("ActualizarComentario/{idComentario}")
def actualizar_comentario(idComentario: int):
    return Actualizar_comentario_controller(idComentario)