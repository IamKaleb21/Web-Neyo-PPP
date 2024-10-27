# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models.conexion import LocalSession, Base
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
import datetime

# Definición del modelo Usuario
class Usuario(Base):
    __tablename__ = "USUARIO"

    IdUsuario = Column(Integer, primary_key=True, index=True)
    Usuario = Column(String(30), unique=True, nullable=False)
    Clave = Column(String(30), unique=True, nullable=False)
    Nombre = Column(String(30), nullable=False)
    Apellido = Column(String(30), nullable=False)
    Fecha_registro = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    Departamento = Column(String(50), nullable=False)
    Provincia = Column(String(50), nullable=False)
    Distrito = Column(String(50), nullable=False)
    Direccion = Column(String(50), nullable=False)
    Correo = Column(String(50), unique=True, nullable=False)

    # Restricciones de unicidad
    __table_args__ = (
        UniqueConstraint("Usuario", "Clave", "Correo", name="uq_usuario_clave_correo"),
    )

# Crear la tabla si no existe
Base.metadata.create_all(bind=LocalSession().bind)

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
