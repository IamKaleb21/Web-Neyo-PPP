from config.conexion import supabase
from fastapi import HTTPException

class InventarioController:
    
    def __init__(self):
        pass
    
    def obtener_inventario(self, id_producto):
        try: 
            # Verificar existencia del registro
            response = supabase.table("inventario").select("cantidad").eq("id_producto", id_producto).execute()
            
            if response.data == None or len(response.data) == 0:
                print("No hay inventario")
                self.crear_inventario(id_producto, 0)
                return float(0)
                
            return response.data[0]["cantidad"]
        
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener el inventario: {str(e)}")

    
    def crear_inventario(self, id_producto, cantidad):
        try:
            response_producto = supabase.table("producto").select("*").eq("id_producto", id_producto).execute()
            if response_producto.data == None or len(response_producto.data) == 0:
                raise HTTPException(status_code=404, detail="El producto no fue encontrado")
            
            response = supabase.table("inventario").insert({
                "id_producto": id_producto,
                "cantidad": cantidad
            }).execute()
            
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear el inventario: {str(e)}")
    
    
    def actualizar_inventario(self, id_producto, cantidad):
        try:
            response = supabase.table("inventario").update({
                "cantidad": cantidad
            }).eq("id_producto", id_producto).execute()
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar el inventario: {str(e)}")
    
    def eliminar_inventario(self, id_producto):
        try: 
            response = supabase.table("inventario").update({
                "cantidad": 0
            }).eq("id_producto", id_producto).execute()
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar el inventario: {str(e)}")
    
    
    def restar_inventario(self, id_producto, cantidad):
        try:
            inventario_actual = self.obtener_inventario(id_producto)
            nuevo_inventario = inventario_actual - cantidad
            if nuevo_inventario < 0:
                raise HTTPException(status_code=400, detail="No hay suficiente inventario")
            self.actualizar_inventario(id_producto, nuevo_inventario)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al restar el inventario: {str(e)}")
    
    
    def sumar_inventario(self, id_producto, cantidad):
        try:
            inventario_actual = self.obtener_inventario(id_producto)
            nuevo_inventario = inventario_actual + cantidad
            self.actualizar_inventario(id_producto, nuevo_inventario)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al sumar el inventario: {str(e)}")
        
    