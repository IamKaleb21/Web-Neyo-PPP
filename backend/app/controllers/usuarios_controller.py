from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Usuario import UsuarioData
from datetime import datetime

# Crud de Usuarios 
def leer_usuarios_funcion():
    try:
        # Consultar todos los usuarios desde la tabla usuario
        usuarios = supabase.table("usuario").select("id_usuario, usuario, nombre, apellido, correo, id_rol").execute()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al obtener usuarios {str(e)}')
    
def leer_usuario_funcion(id):
    try: 
        # buscar un usuario por respecto a su id
        usuario = supabase.table("usuario").select("id_usuario, usuario, nombre, apellido, correo, id_rol").eq("id_usuario", id).execute()
        #  Verificar si esta el usuario o no
        if not usuario.data :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        else :
            return usuario
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al procesar la solicitud : {str(e)}')
    
def ingresar_usuario_funcion(user: UsuarioData):
    try: 
        # Verificar si el usuario ya existe
        usuario_existente = supabase.table("usuario").select("id_usuario").eq("usuario", user.usuario).execute()
        if usuario_existente.data :
            raise HTTPException(status_code=400, detail="Usuario ya existe")
        # Si no existe, inserta el nuevo usuario
        usuario = supabase.table("usuario").insert({
            "usuario": user.usuario,
            "clave": user.clave,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "departamento" : user.departamento,
            "provincia" : user.provincia,
            "distrito" : user.distrito,
            "direccion" : user.direccion,
            "correo" : user.correo,
            "id_rol" : user.id_rol.value
        }).execute()
        usuario_data = usuario.data[0]
        supabase.table("telefono").insert({
            "numero":user.telefono,
            "id_usuario": usuario_data['id_usuario']
        }).execute()
        
        # Ingresas a un nuevo usuario en Auth cuando te registras
        usuarioAut=supabase.auth.sign_up( 
            {
                "email" : user.correo,
                "password" : user.clave,
                "options" : {
                    "data" : {
                        "Nombre" : user.nombre,
                        "Apellido" : user.apellido,
                        "Departamento" : user.departamento,
                        "Provincia" : user.provincia,
                        "Distrito" : user.distrito,
                    }
                }
            }
        )
        usuarioFinal = (supabase.table("usuario").update({"principal": usuarioAut.user.id}).eq("id_usuario", usuario_data['id_usuario']).execute())
        
        return usuarioFinal
    # Manejo específico de HTTPException
    except HTTPException as http_err:
        raise http_err
    # Otras excepciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

def actualizar_usuario_funcion(id: int, user : UsuarioData):
    try:
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
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

def eliminar_usuario_funcion(id: int):
    try:
        # Verificar si el usuario se encuentra en la base de datos 
        bandera = False
        id_usuarios = supabase.table("usuario").select("id_usuario").execute()
        for usuario in id_usuarios.data:
            if id == usuario["id_usuario"] :
                bandera = True
        if bandera == True :
            # Eliminar de todos las tablas donde se encuentra el id_usuario
            telefonosEliminados = supabase.table("telefono").delete().eq("id_usuario",id).execute()
            carritoEliminado = supabase.table("carrito_compra").delete().eq("id_usuario",id).execute()
            usuarioEliminado = supabase.table("usuario").delete().eq("id_usuario",id).execute()
            return usuarioEliminado 
        else :
            # Si no se encuentra salta un error con el codigo responsable
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")