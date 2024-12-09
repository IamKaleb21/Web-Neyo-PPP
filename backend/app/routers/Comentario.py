from fastapi import APIRouter,Path
from Schemas.Comentario import ComentarioData
from controllers.Comentario_controller import *

comentario = APIRouter(prefix="/comentario",
                     tags=["Comentario"],
                      responses={404: {"mensaje" : "No encontrado"}})


# URL -Comentario funciones
@comentario.post("/crearComentario", status_code=201)
def crear_comentario(comentario: ComentarioData):
    return crear_cometario_controller(comentario)

# Recuperar comentarios de un respectivo producto
@comentario.get("/RecuperarProducto/{idProducto:int}")
def mostrar_comentario_producto(idProducto: int  = Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return mostrar_comentarios_producto_controller(idProducto)

# Recuperar comentarios de un respectivo cliente
@comentario.get("/RecuperarCliente/{idCliente:int}")
def mostrar_comentario_cliente(idCliente: int  = Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return mostrar_comentarios_cliente_controller(idCliente)

# Eliminar un comentario
@comentario.delete("/Eliminar/{idComentario: int}", status_code=204)
def eliminar_comentario(idComentario: int = Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return eliminar_comentario_controller(idComentario)

# Eliminar todos los comentarios de un usuario
@comentario.delete("/EliminarTodo/{idCliente: int}")
def eliminar_comentarios_cliente(idCliente: int = Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return eliminar_comentarios_controller_cliente(idCliente)
# Actualizar comentario
@comentario.put("ActualizarComentario/{idComentario}")
def actualizar_comentario(comentarioActualizado: ComentarioData,idComentario: int = Path(..., gt=0, description="El ID debe ser un entero mayor a cero")):
    return Actualizar_comentario_controller(idComentario, comentarioActualizado)