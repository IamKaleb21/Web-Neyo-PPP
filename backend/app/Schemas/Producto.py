from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from decimal import Decimal

class ProductoData(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    url_imagen: Optional[str] = None
    id_modelo: Optional[int] = None
    id_categoria: Optional[int] = None
    id_estado: Optional[int] = None