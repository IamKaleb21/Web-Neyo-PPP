# models.py
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Crear una clase base para los modelos
Base = declarative_base()

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
