from fastapi import APIRouter
from Schemas.Producto import ProductoData
from controllers.productos_controller import ProductoController

productos = APIRouter(prefix="/productos",
                     tags=["Productos"],
                     responses={404: {"mensaje" : "No encontrado"}})

producto_controller = ProductoController()


@productos.get("/")
def obtener_productos():
    return producto_controller.leer_productos()


@productos.get("/{id:int}")
def obtener_producto(id: int):
    return producto_controller.leer_producto(id)


@productos.post("/insertar/")
async def insertar_producto(producto: ProductoData, cantidad: int):
    return producto_controller.insertar_producto(producto, cantidad)

@productos.put("/actualizar/{id}")
def actualizar_producto(id : int , producto : ProductoData):
    return producto_controller.actualizar_producto(id , producto)


@productos.delete("/eliminar/{id}")
def eliminar_producto(id : int) :
    return producto_controller.eliminar_producto(id)

