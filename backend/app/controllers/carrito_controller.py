from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Producto import ProductoData


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
    
    def agregar_carrito(self, id_usuario, id_producto, cantidad):
        
        
        
        try: 
            response = supabase.table("detalle_carrito").insert({
                "cantidad": cantidad,
                "id_producto": id_producto,
                "id_carrito": self.obtener_id(id_usuario)
            }).execute()
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al agregar al carrito: {str(e)}")

        return response.data[0]
        
        
    