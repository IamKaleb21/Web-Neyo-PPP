from config.conexion import supabase
from fastapi import HTTPException
from Schemas.Producto import ProductoData

class ProductoController:
    def __init__(self):
        # Inicialización si es necesario
        pass

    def leer_productos(self):
        try:
            productos = supabase.table("producto").select("*").execute()
            return productos.data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al leer productos: {str(e)}")


    def leer_producto(self, id: int):
        try:
            producto = supabase.table("producto").select("*").eq("id_producto", id).execute()
            if not producto.data:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            return producto.data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al leer el producto: {str(e)}")


    def insertar_producto(self, producto: ProductoData, cantidad: int):
        try:
            response = supabase.table("producto").insert({
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "url_imagen": producto.url_imagen,
                "id_modelo": producto.id_modelo,
                "id_categoria": producto.id_categoria,
                "id_estado": producto.id_estado
            }).execute()
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al insertar el producto: {str(e)}")
        nuevo_producto = response.data[0]
        
        self.crear_inventario(nuevo_producto["id_producto"], cantidad)
        return nuevo_producto
    
    def crear_inventario(self, id_producto, cantidad):
        try:
            # Inserción del inventario
            response = supabase.table("inventario").insert({
                "cantidad": cantidad,
                "id_producto": id_producto
            }).execute()
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear el inventario: {str(e)}")
            
        
    def actualizar_producto(self, id: int, producto : ProductoData):
        resultado = supabase.table("producto").select("*").eq("id_producto", id).execute()
        
        # Verifica si el producto no existe
        if not resultado.data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        producto_actualizado = supabase.table("producto").update({
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "url_imagen": producto.url_imagen,
            "id_modelo": producto.id_modelo,
            "id_categoria": producto.id_categoria,
            "id_estado": producto.id_estado
        }).eq("id_producto", id).execute()
        
        return producto_actualizado
        
    def eliminar_producto(self, id: int):
        
        # Busca directamente el producto por su ID
        resultado = supabase.table("producto").select("id_producto").eq("id_producto", id).execute()
        
        # Verifica si el producto existe
        if not resultado.data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Elimina el producto
        usuario_eliminado = supabase.table("producto").delete().eq("id_producto", id).execute()
        
        return usuario_eliminado