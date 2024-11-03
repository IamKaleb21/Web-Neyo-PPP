from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class RolUsuario(Enum):
    Admin = 1
    prueba = 2

class UsuarioData(BaseModel):
    usuario: str  
    clave: str  
    nombre: str  
    apellido: str  
    fecha_registro: Optional[datetime] = None  
    departamento: str
    provincia: str  
    distrito: str  
    direccion: str  
    correo: EmailStr
    id_rol : RolUsuario = RolUsuario.prueba


