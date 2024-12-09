from fastapi import APIRouter
from controllers.pago_controller import PagoController
from Schemas.pago import PagoData

pago = APIRouter(prefix="/pago", tags=["Pago"], responses={404: {"mensaje": "No encontrado"}})

pago_controller = PagoController()

@pago.post("/crear/")
def crear_pago(pago: PagoData):
    return pago_controller.crear_pago(pago)

