from fastapi import APIRouter
from controllers.carrito_controller import CarritoController
from Schemas.detalle_carrito import DetalleCarritoData


carrito = APIRouter(prefix="/carrito",
                     tags=["Carrito"],
                     responses={404: {"mensaje" : "No encontrado"}})

carrito_controller = CarritoController()

@carrito.get("/{id:int}")
def obtener_id(id: int):
    return carrito_controller.obtener_id(id)

@carrito.post("/agregar/")
def agregar_producto(detalle_carrito: DetalleCarritoData):
    return carrito_controller.agregar_producto(detalle_carrito)

@carrito.get("/obtener/{id:int}")
def obtener_carrito(id):
    return carrito_controller.obtener_carrito(id)

@carrito.delete("/quitar/")
def quitar_producto(id_usuario: int, id_producto: int):
    return carrito_controller.quitar_producto(id_usuario, id_producto)

