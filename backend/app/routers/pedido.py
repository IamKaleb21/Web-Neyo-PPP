from fastapi import APIRouter
from controllers.pedido_controller import PedidoController


pedido = APIRouter(prefix="/pedido", tags=["Pedido"], responses={404: {"mensaje": "No encontrado"}})

pedido_controller = PedidoController()

@pedido.post("/crear/")
def crear_pedido(id_usuario: int):
    return pedido_controller.crear_pedido(id_usuario)

@pedido.get("/leer/")
def obtener_pedidos(id_usuario: int):
    return pedido_controller.obtener_pedidos(id_usuario)

@pedido.get("/leer/{id}")
def obtener_detalle_pedido(id: int):
    return pedido_controller.obtener_detalle_pedido(id)

@pedido.delete("/cancelar/{id}")
def cancelar_pedido(id: int):
    return pedido_controller.cancelar_pedido(id)

@pedido.get("/estado-actual/{id}")
def obtener_estado_actual(id: int):
    return pedido_controller.obtener_estado_actual(id)

@pedido.post("/historial/")
def crear_historial_estado(id_pedido: int):
    return pedido_controller.crear_historial_estado(id_pedido)

@pedido.put("/historial/{id_pedido}")
def actualizar_historial_estado(id_pedido: int, id_estado: int):
    return pedido_controller.actualizar_historial_estado(id_pedido, id_estado)