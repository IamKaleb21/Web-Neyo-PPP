from pydantic import BaseModel
from typing import Optional

from decimal import Decimal

class DetalleCarritoData(BaseModel):
    cantidad: int
    id_producto: int
    id_usuario: int
    