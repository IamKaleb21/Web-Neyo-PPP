from fastapi import APIRouter
from controllers.carrito_controller import CarritoController

carrito = APIRouter(prefix="/carrito",
                     tags=["Carrito"],
                     responses={404: {"mensaje" : "No encontrado"}})

carrito_controller = CarritoController()

@carrito.get("/{id:int}")
def obtener_id(id: int):
    return carrito_controller.obtener_id(id)

# @carrito.post("/agregar/")
