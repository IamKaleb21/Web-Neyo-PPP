from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Producto import ProductoData
from controllers.carrito_controller import CarritoController
from controllers.inventario_controller import InventarioController

from controllers.productos_controller import ProductoController

from enum import Enum

carrito_controller = CarritoController()
inventario_controller = InventarioController()
producto_controller = ProductoController()


class estado(Enum):
    INDEFINIDO = 1
    EN_PROCESO = 2
    ENVIADO = 3
    ENTREGADO = 4
    CANCELADO = 5


class PedidoController:
    def __init__(self):
        # Inicialización si es necesario
        pass
    
    def crear_pedido(self, id_usuario):
        try: 
            carrito = carrito_controller.obtener_carrito(id_usuario)
            if len(carrito) == 0:
                raise HTTPException(status_code=400, detail="No hay productos en el carrito")
            for pedido in carrito:
                print(pedido)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener el carrito: {str(e)}")
        
        #verificar si hay suficiente inventario
        try:
            for item in carrito:
                inventario = inventario_controller.obtener_inventario(item["id_producto"])
                if inventario < item["cantidad"]:
                    raise HTTPException(status_code=400, 
                detail=f"No hay suficiente inventario del producto con id: {item['id_producto']}. Inventario actual: {inventario}. Cantidad solicitada: {item['cantidad']}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al verificar el inventario: {str(e)}")
            
        #Crear el pedido
        try:
            response = supabase.table("pedido").insert({
                "id_usuario": id_usuario,
                "total": 0,
                "id_estado_pedido": 2
            }).execute()
            nuevo_pedido = response.data[0]
            id_pedido = nuevo_pedido["id_pedido"]
            
            total = 0
            for item in carrito:
                producto = producto_controller.leer_producto(item["id_producto"])
                
                # Restar el inventario
                inventario_controller.restar_inventario(item["id_producto"], item["cantidad"])
                
                # Crear el detalle del pedido
                response = supabase.table("detalle_pedido").insert({
                    "cantidad": item["cantidad"],
                    "precio_venta": producto["precio"],
                    "subtotal": item["cantidad"] * producto["precio"],
                    "id_pedido": id_pedido,
                    "id_producto": item["id_producto"]   
                }).execute()
                total += item["cantidad"] * producto["precio"]
                carrito_controller.vaciar_carrito(id_usuario)
            
            # Actualizar el total del pedido
            response = supabase.table("pedido").update({
                "total": total
            }).eq("id_pedido", id_pedido).execute()
            
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear el pedido: {str(e)}")
        
        
        return nuevo_pedido
    
    def obtener_pedidos(self, id_usuario):
        try:
            response = supabase.table("pedido").select("*").eq("id_usuario", id_usuario).execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=500, 
        detail=f"Error al obtener los pedidos: {str(e)}")
    
    
    def obtener_detalle_pedido(self, id_pedido):
        try:
            response_detalle = supabase.table("detalle_pedido").select("*").eq("id_pedido", id_pedido).execute()
            if len(response_detalle.data) == 0:
                raise HTTPException(status_code=404, 
        detail="No se encontró el detalle del pedido solicitado")
            
            for item in response_detalle.data:
                producto = producto_controller.leer_producto(item["id_producto"])
                item["producto"] = producto
            
            return response_detalle.data
        
        except Exception as e:
            raise HTTPException(status_code=500, 
        detail=f"Error al obtener el detalle del pedido: {str(e)}")
        
    def cancelar_pedido(self, id_pedido):
        try: 
            response = supabase.table("detalle_pedido").select("detalle_pedido, cantidad, id_producto").eq("id_pedido", id_pedido).execute()
            
            if len(response.data) == 0:
                raise HTTPException(status_code=404, detail="No se encontró el pedido indicado")
            
            for item in response.data:
                # Restaurar inventario
                inventario_controller.sumar_inventario(item["id_producto"], item["cantidad"])
            
                # # Borrar el detalle del pedido
                # response = supabase.table("detalle_pedido").delete().eq("id_pedido", id_pedido).execute()
            
            # cancelar el pedido
            self.actualizar_historial_estado(id_pedido, estado.CANCELADO.value)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al cancelar el pedido: {str(e)}")
        
    def existe_historial(self, id_pedido):
        try:
            response = supabase.table("historial_pedido").select("*").eq("id_pedido", id_pedido).execute()
            
            if len(response.data) == 0:
                return False
            else: return True
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al verificar el historial del pedido: {str(e)}")
        
    def obtener_estado_actual(self, id_pedido):
        try:
            response = supabase.table("pedido").select("id_estado_pedido").eq("id_pedido", id_pedido).execute()
            return response.data[0]["id_estado_pedido"]
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener el estado actual del pedido: {str(e)}")
    
    def crear_historial_estado(self, id_pedido):
        try:
            if self.existe_historial(id_pedido):
                return {"mensaje": "El historial ya existe"}
            
            response = supabase.table("historial_pedido").insert({
                "id_pedido": id_pedido,
                "id_estado_actual": estado.EN_PROCESO.value,
                "id_estado_anterior": estado.INDEFINIDO.value
            }).execute()
            
            return response.data[0]
        
        except Exception as e:
            raise HTTPException(status_code=500, 
            detail=f"Error al crear el historial del pedido: {str(e)}")
    
    def obtener_historial_estado(self, id_pedido):
        try:
            if not self.existe_historial(id_pedido):
                raise HTTPException(status_code=404, detail="No existe historial del pedido")
            
            response = supabase.table("historial_pedido").select("*").eq("id_pedido", id_pedido).execute()
            return response.data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener el historial del pedido: {str(e)}")
    
    def actualizar_historial_estado(self, id_pedido, nuevo_estado):
        try:
            if not self.existe_historial(id_pedido):
                raise HTTPException(status_code=404, detail="No existe historial del pedido")
            
            estado_actual = self.obtener_estado_actual(id_pedido)
            
            # Actualizar el historial del pedido
            response = supabase.table("historial_pedido").insert({
                "id_pedido": id_pedido,
                "id_estado_actual": nuevo_estado,
                "id_estado_anterior": estado_actual
            }).execute()
            
            # Actualizar el estado del pedido
            supabase.table("pedido").update({
                "id_estado_pedido": nuevo_estado
            }).eq("id_pedido", id_pedido).execute()
            
        except Exception as e:
            raise HTTPException(status_code=500, 
            detail=f"Error al actualizar el historial del pedido: {str(e)}")
    
    def existe_pedido(self, id_pedido):
        try:
            response = supabase.table("pedido").select("*").eq("id_pedido", id_pedido).execute()
            if response.data != None and len(response.data) > 0:
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al verificar el pedido: {str(e)}")