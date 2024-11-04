# controllers/auth_controller.py
from supabase import create_client, Client
from fastapi import HTTPException
import config

# Inicializamos el cliente de Supabase
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

class AuthController:
    def iniciar_sesion(self, email: str, password: str):
        try:
            # Intentar iniciar sesión con correo y contraseña
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            # Verificar si hay algún error en la respuesta
            if response.get("error"):
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            # Retornamos el token de acceso y detalles del usuario
            return {
                "access_token": response["data"]["access_token"],
                "refresh_token": response["data"]["refresh_token"],
                "user": response["data"]["user"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error en el servidor")
