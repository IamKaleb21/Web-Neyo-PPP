from fastapi import APIRouter
from controllers.inventario_controller import InventarioController

inventario = APIRouter(prefix="/inventario",
                       tags=["Inventario"],
                          responses={404: {"mensaje": "No encontrado"}})

inventario_controller = InventarioController()

@inventario.get("/{id:int}")
def obtener_inventario(id: int):
    return inventario_controller.obtener_inventario(id)
    
@inventario.put("/actualizar/{id}")
def actualizar_inventario(id: int, cantidad: int):
    return inventario_controller.actualizar_inventario(id, cantidad)

@inventario.delete("/eliminar/{id}")
def eliminar_inventario(id: int):
    return inventario_controller.eliminar_inventario(id)

@inventario.put("/restar/{id}")
def restar_inventario(id: int, cantidad: int):
    return inventario_controller.restar_inventario(id, cantidad)

@inventario.put("/sumar/{id}")
def sumar_inventario(id: int, cantidad: int):
    return inventario_controller.sumar_inventario(id, cantidad)