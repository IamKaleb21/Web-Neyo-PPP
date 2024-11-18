from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Producto import ProductoData
from controllers.inventario_controller import InventarioController
from Schemas.detalle_carrito import DetalleCarritoData



inventario_controller = InventarioController()

class CarritoController:
    def __init__(self):
        # Inicialización si es necesario
        pass

    def crear_carrito(self, id_usuario):
        try:
            # Inserción del carrito
            response = supabase.table("carrito_compra").insert({
                "id_usuario": id_usuario
            }).execute()
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear el inventario: {str(e)}")
    
    def obtener_id(self, id_usuario):
        try:
            response = supabase.table("carrito_compra").select("id_carrito").eq("id_usuario", id_usuario).execute()
            
            # Validar si response.data no tiene valores
            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=404, detail="No se encontró un carrito para el usuario especificado")
            
            carrito = response.data[0]
            
            return carrito["id_carrito"]
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener el id: {str(e)}")
    
    def obtener_carrito(self, id_usuario):
        try:
            id_carrito = self.obtener_id(id_usuario)
            print(id_carrito)
            response = supabase.table("detalle_carrito").select("*").eq("id_carrito", id_carrito).execute()
            
            return response.data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener el carrito: {str(e)}")
    
    def agregar_producto(self, detalle_carrito: DetalleCarritoData):
        inventario = inventario_controller.obtener_inventario(detalle_carrito.id_producto)
        
        if inventario < detalle_carrito.cantidad:
            raise HTTPException(status_code=400, detail=f"No hay suficiente inventario. Inventario actual: {inventario}. Cantidad solicitada: {detalle_carrito.cantidad}")
        
        
        try: 
            response = supabase.table("detalle_carrito").insert({
                "cantidad": detalle_carrito.cantidad,
                "id_producto": detalle_carrito.id_producto,
                "id_carrito": self.obtener_id(detalle_carrito.id_usuario)
            }).execute()
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al agregar al carrito: {str(e)}")

        return response.data[0]
        
    def quitar_producto(self, id_usuario, id_producto):
        try:
            id_carrito = self.obtener_id(id_usuario)
            response = supabase.table("detalle_carrito").delete().eq("id_carrito", id_carrito).eq("id_producto", id_producto).execute()
            
            return response.data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al quitar del carrito: {str(e)}")
    
    # TODO: Validar que no se pueda agregar un producto que ya está en el carrito