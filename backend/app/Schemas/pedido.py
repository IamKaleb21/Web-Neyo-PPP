from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from decimal import Decimal
    
class PedidoData(BaseModel):
    total: float
    id_usuario: int
    id_estado_pedido: int