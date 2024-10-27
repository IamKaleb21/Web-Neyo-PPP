from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.conexion import LocalSession  # Importar la sesión de la base de datos
from models.Usuarios import Usuario
from Schemas.Usuario import UsuarioId, UsuarioData
import datetime
# Inicializa la aplicación FastAPI
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/usuarios/")
def read_usuarios(db: Session = Depends(get_db)):
    # Consultar todos los registros de la tabla USUARIO
    usuarios = db.query(Usuario).all()  # Recupera todos los registros de la tabla USUARIO
    return [{"ID": usuario.IdUsuario, "Usuario": usuario.Usuario, "Nombre": usuario.Nombre, "Apellido": usuario.Apellido} for usuario in usuarios]

@app.get("/usuario/{id:int}")  # Asegúrate de que la ruta esté bien definida
def read_usuario(id: int, db: Session = Depends(get_db)):  # Define el tipo de id
    usuario = db.query(Usuario).filter(Usuario.IdUsuario == id).first()  # Llama a first() correctamente
    if usuario is None:  # Manejo de caso en que no se encuentra el usuario
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "ID": usuario.IdUsuario,
        "Usuario": usuario.Usuario,
        "Nombre": usuario.Nombre,
        "Apellido": usuario.Apellido,
        "Departamento": usuario.Departamento,
        "Provincia": usuario.Provincia,
        "Distrito": usuario.Distrito,
        "Direccion": usuario.Direccion,
        "Correo": usuario.Correo
    }

@app.post("/ingresarUsuario", response_model=UsuarioId)
def crear_usuario(user: UsuarioData, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter(Usuario.Usuario == user.Usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Encriptar la clave usando hashlib
    hashed_password = hashlib.sha256(user.Clave.encode()).hexdigest()

    new_user = Usuario(
        Usuario=user.Usuario,
        Clave=hashed_password,
        Nombre=user.Nombre,
        Apellido=user.Apellido,
        Fecha_registro=user.Fecha_registro or datetime.utcnow(),
        Departamento=user.Departamento,
        Provincia=user.Provincia,
        Distrito=user.Distrito,
        Direccion=user.Direccion,
        Correo=user.Correo
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresca la instancia de nuevo usuario

    return {
        "id": new_user.IdUsuario,
        "Usuario": new_user.Usuario,
        "Nombre": new_user.Nombre,
        "Apellido": new_user.Apellido,
        "Departamento": new_user.Departamento,
        "Provincia": new_user.Provincia,
        "Distrito": new_user.Distrito,
        "Direccion": new_user.Direccion,
        "Correo": new_user.Correo
    }