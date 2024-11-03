from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Usuario import UsuarioData
from datetime import datetime

# Crud de Usuarios 
def leer_usuarios_funcion():
    usuarios = supabase.table("usuario").select("*").execute()
    return usuarios

def leer_usuario_funcion(id):
    usuario = supabase.table("usuario").select("*").eq("id_usuario", id).execute()
    if not usuario.data :
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else :
        return usuario
def ingresar_usuario_funcion(user: UsuarioData): 
    user.fecha_registro = datetime.now()
    usuario = supabase.table("usuario").insert({
        "usuario": user.usuario,
        "clave": user.clave,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "fecha_registro" : user.fecha_registro.strftime("%Y-%m-%dT%H:%M:%S"),
        "departamento" : user.departamento,
        "provincia" : user.provincia,
        "distrito" : user.distrito,
        "direccion" : user.direccion,
        "correo" : user.correo,
        "id_rol" : user.id_rol.value
    }).execute()
    return usuario

def actualizar_usuario_funcion(id: int, user : UsuarioData):
    user.fecha_registro = datetime.now()
    bandera = False
    id_usuarios = supabase.table("usuario").select("id_usuario").execute()
    for usuario in id_usuarios.data:
        if id == usuario["id_usuario"] :
            bandera = True
    if bandera == True : 
        usuario_actualizado = supabase.table("usuario").update({
            "usuario": user.usuario,
            "clave": user.clave,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "fecha_registro" : user.fecha_registro.strftime("%Y-%m-%dT%H:%M:%S"),
            "departamento" : user.departamento,
            "provincia" : user.provincia,
            "distrito" : user.distrito,
            "direccion" : user.direccion,
            "correo" : user.correo,
            "id_rol" : user.id_rol.value
        }).eq("id_usuario",id).execute()
        return usuario_actualizado
    else :
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
def eliminar_usuario_funcion(id: int):
    bandera = False
    id_usuarios = supabase.table("usuario").select("id_usuario").execute()
    for usuario in id_usuarios.data:
        if id == usuario["id_usuario"] :
            bandera = True
    if bandera == True :
        usuarioEliminado = supabase.table("usuario").delete().eq("id_usuario",id).execute()
        return usuarioEliminado 
    else :
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
