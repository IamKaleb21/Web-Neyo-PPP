from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PagoData(BaseModel):
    monto: float
    id_pedido: int
    id_metodo_pago: int
    id_estado_pago: int
    referencia: Optional[str] = None

