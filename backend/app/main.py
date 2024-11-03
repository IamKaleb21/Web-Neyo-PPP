from fastapi import FastAPI, Depends, HTTPException
from models.conexion import supabase  # Importar la sesión de la base de datos
from Schemas.Usuario import UsuarioData
from datetime import datetime



# Inicializa la aplicación FastAPI
app = FastAPI()

@app.get("/")
def read_usuarios():
    return {
        "hola" :"usuario1"
    }        

@app.get("/usuarios/")
def read_usuarios():
    informacion = supabase.table("usuario").select("*").execute()
    return informacion    

@app.get("/usuario/{id:int}")  
def read_usuario(id: int):  
    usuario = supabase.table("usuario").select("*").eq("id_usuario",id).execute()
    
    if not usuario.data :
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else :
        return usuario

@app.post("/ingresarUsuario/")
def ingresar_usuario(user: UsuarioData):
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

@app.put("/actualizarUsuario/{id}")
def actualizar_usuario(id : int, user: UsuarioData):
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

@app.delete("/eliminarUsuario/{id}")
def eliminar_usuario(id : int):
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
    