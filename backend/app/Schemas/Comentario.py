from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ComentarioData(BaseModel) :
    contenido: str
    valoracion: str
    id_producto: int

