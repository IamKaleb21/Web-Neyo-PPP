from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

class UsuarioData(BaseModel):
    Usuario: str  
    Clave: str  
    Nombre: str  
    Apellido: str  
    Fecha_registro: Optional[datetime] = None  
    Departamento: str
    Provincia: str  
    Distrito: str  
    Direccion: str  
    Correo: EmailStr  
    
class UsuarioId(UsuarioData):
    id : int

