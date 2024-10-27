# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models.conexion import LocalSession  # Importar la sesión de la base de datos
from models.Usuarios import Usuario

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
