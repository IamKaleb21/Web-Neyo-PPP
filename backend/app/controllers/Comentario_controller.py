from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Comentario import ComentarioData
from datetime import datetime
import logging

#Crear un nuevo comentario

def crear_cometario_controller(comentario: ComentarioData):
    try: 
        usuario_sesion = supabase.auth.get_session()
        if not usuario_sesion:
            raise HTTPException(status_code=404, detail="No ha iniciado sesión")
        else:
            principal_sesion = usuario_sesion.user.id

            usuario_public= supabase.table("usuario").select("*").eq("principal",principal_sesion).execute()

            comentario = supabase.table("comentario").insert({
            "contenido": comentario.contenido,
            "valoracion": comentario.valoracion,
            "id_producto": comentario.id_producto,
            "id_usuario": usuario_public.data[0]["id_usuario"], 
        }).execute()
        return comentario
    except HTTPException as http_err:
        raise http_err
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
    except HTTPException as http_err:
        raise http_err
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
    except HTTPException as http_err:
        raise http_err
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
    except HTTPException as http_err:
        raise http_err
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
    except HTTPException as http_err:
        raise http_err
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
# Actualizar un comentario
def Actualizar_comentario_controller(idComentario: int, comentarioActualizado: ComentarioData):
    try:
        usuario_sesion = supabase.auth.get_session()
        if not usuario_sesion:
            raise HTTPException(status_code=404, detail="No ha iniciado sesión")
        else:
            principal_sesion= usuario_sesion.user.id
            # Recuperar el usuario de la tabla publica 
            usuario_public= supabase.table("usuario").select("*").eq("principal",principal_sesion).execute()


            comentarioActualizado = supabase.table("comentario").update({
                "contenido": comentarioActualizado.contenido,
                "valoracion": comentarioActualizado.valoracion,
                "id_usuario": usuario_public.data[0]["id_usuario"],
        }).eq("id_comentario",idComentario).execute()
        
        if not comentarioActualizado.data:
            raise HTTPException(status_code=404, detail="No Existe el comentario")
        return comentarioActualizado
    except HTTPException as http_err:
        raise http_err
    except Exception as e :
        logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
