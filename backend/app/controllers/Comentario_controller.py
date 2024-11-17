from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Comentario import ComentarioData
from datetime import datetime
import logging

#Crear un nuevo comentario

def crear_cometario_controller(comentario: ComentarioData):
    try: 
        comentario = supabase.table("comentario").insert({
            "contenido": comentario.contenido,
            "valoracion": comentario.valoracion,
            "id_producto": comentario.id_producto,
            "id_usuario": comentario.id_usuario, 
        }).execute()
        return comentario
    except Exception as e:
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

#  Obtener los comentarios de un producto

def mostrar_comentarios_producto_controller(idProducto: int):
    try:
        informacion = supabase.table("comentario").select("contenido, valoracion, fecha_registro, id_usuario").eq("id_producto", idProducto).execute()
        if not informacion.data :
            raise HTTPException(status_code=404, detail="No hay comentarios de ese Producto")
        else: 
            return informacion
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
            
#Obtener los comentarios de un cliente

def mostrar_comentarios_cliente_controller(idCliente: int):
    try:
        informacion = supabase.table("comentario").select("contenido, valoracion, fecha_registro, id_usuario").eq("id_usuario", idCliente).execute()
        if not informacion.data :
            raise HTTPException(status_code=404, detail="No hay comentarios de ese cliente")
        else: 
            return informacion
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")


# Eliminar un comentario 
def eliminar_comentario_controller(idComentario: int):
    try:
        comentarioEliminado = supabase.table("comentario").delete().eq('id_comentario',idComentario).execute()
        if not comentarioEliminado.data:
            raise HTTPException(status_code=404, detail="No Existe el comentario")
        else:
            return comentarioEliminado
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
# Eliminar todos los comentarios de un usuario
def eliminar_comentarios_controller_cliente(idCliente: int):
    try:
        comentariosEliminados = supabase.table("comentario").delete().eq('id_usuario',idCliente).execute()
        if not comentariosEliminados.data:
            raise HTTPException(status_code=404, detail="No Existe el comentario")
        else:
            return comentariosEliminados
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
# Actualizar un comentario
def Actualizar_comentario_controller(idComentario: int, comentarioActualizado: ComentarioData):
    try:
        comentarioActualizado = supabase.table("comentario").update({
            "contenido": comentarioActualizado.contenido,
            "valoracion": comentarioActualizado.valoracion,
            "id_producto": comentarioActualizado.id_producto,
            "id_usuario": comentarioActualizado.id_usuario,
        }).eq("id_comentario",idComentario).execute()
        
        if not comentarioActualizado.data:
            raise HTTPException(status_code=404, detail="No Existe el comentario")
        return comentarioActualizado
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
