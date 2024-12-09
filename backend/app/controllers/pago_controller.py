from config.conexion import supabase
from fastapi import HTTPException
from Schemas.pago import PagoData
from controllers.pedido_controller import PedidoController

from enum import Enum

class metodo(Enum):
    INDEFINIDO = 1
    EFECTIVO = 2
    TRANSFERENCIA = 3
    PAGOEFECTIVO = 4
    OTRO = 5

class estado(Enum):
    INDEFINIDO = 1
    PENDIENTE = 2
    COMPLETADO = 3
    FALLIDO = 4
    CANCELADO = 5

pedido_controller = PedidoController()

class PagoController:
    def __init__(self):
        pass
    
    def crear_pago(self, pago: PagoData):
        try:
            print("1.")
            print(pago.id_pedido)
            # Verifica la existencia del pedido
            if not pedido_controller.existe_pedido(pago.id_pedido):
                raise HTTPException(status_code=400, 
                    detail="El pedido no fue encontrado")
            
            # Verifica si el pedido ya tiene un pago asociado
            if self.pago_asociado(pago.id_pedido):
                raise HTTPException(status_code=400, 
                    detail="El pedido ya tiene un pago asociado")
            
            # Verifica si la referencia ya fue utilizada
            if self.referencia_duplicada(pago.referencia):
                raise HTTPException(status_code=400, 
                    detail="La referencia ya fue utilizada")
            
            response = supabase.table("pago").insert({
                "monto": pago.monto,
                "id_pedido": pago.id_pedido,
                "id_metodo_pago": pago.id_metodo_pago,
                "id_estado_pago": pago.id_estado_pago,
                "referencia": pago.referencia
            }).execute()
            
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al crear el pago: {str(e)}")
        
        
    def referencia_duplicada(self, referencia: str):
        try:
            response = supabase.table("pago").select("*").eq("referencia", referencia).execute()
        
            if response.data != None and len(response.data) > 0:
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al verificar la referencia: {str(e)}")
    
    def pago_asociado(self, id_pedido: int):
        try:
            response = supabase.table("pago").select("*").eq("id_pedido", id_pedido).execute()
            
            if response.data != None and len(response.data) > 0:
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al verificar el pago asociado: {str(e)}")
    
    def obtener_pago(self, id_pago: int):
        try:
            if not self.existe_pago(id_pago):
                raise HTTPException(status_code=404, 
                detail="El pago no fue encontrado")
            
            response = supabase.table("pago").select("*").eq("id_pago", id_pago).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al obtener el pago: {str(e)}")
    
    def obtener_pago_pedido(self, id_pedido: int):
        try:
            if not pedido_controller.existe_pedido(id_pedido):
                raise HTTPException(status_code=404, 
                    detail="El pedido no fue encontrado")
            
            response = supabase.table("pago").select("*").eq("id_pedido", id_pedido).execute()
            return response.data
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al obtener el pago del pedido: {str(e)}")
    
    def existe_pago(self, id_pago: int):
        try:
            response = supabase.table("pago").select("*").eq("id_pago", id_pago).execute()
            if response.data != None and len(response.data) > 0:
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, 
                detail=f"Error al verificar el pago: {str(e)}")
    
    def actualizar_pago(self, id_pago: int, nuevo_estado: int):
        try:
            if not self.existe_pago(id_pago):
                raise HTTPException(status_code=404, detail="El pago no fue encontrado")
            
            response = supabase.table("pago").update({
                "id_estado_pago": nuevo_estado
            }).eq("id_pago", id_pago).execute()
            
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar el pago: {str(e)}")
        
    