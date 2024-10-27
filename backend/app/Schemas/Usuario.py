from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

class UsuarioData(BaseModel):
    Usuario: constr(max_length=30)  # Limita la longitud a 30 caracteres
    Clave: constr(max_length=30)  # Limita la longitud a 30 caracteres
    Nombre: constr(max_length=30)  # Limita la longitud a 30 caracteres
    Apellido: constr(max_length=30)  # Limita la longitud a 30 caracteres
    Fecha_registro: Optional[datetime] = None  # Fecha opcional al crear
    Departamento: constr(max_length=50)  # Limita la longitud a 50 caracteres
    Provincia: constr(max_length=50)  # Limita la longitud a 50 caracteres
    Distrito: constr(max_length=50)  # Limita la longitud a 50 caracteres
    Direccion: constr(max_length=50)  # Limita la longitud a 50 caracteres
    Correo: EmailStr  # Valida que sea un correo electrónico
    
class UsuarioId(UsuarioData):
    id : int

