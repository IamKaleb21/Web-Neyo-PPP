from fastapi import HTTPException
from config.conexion import supabase
import logging

class AuthController:
    def iniciar_sesion(self, email: str, password: str):
        logging.info(f"Iniciando sesión para el usuario: {email}")
        try:
            # Intentar iniciar sesión con correo y contraseña
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            # Verificar si la autenticación fue exitosa
            if response and response.session:
                # Extraer los tokens de sesión y los datos del usuario
                access_token = response.session.access_token
                refresh_token = response.session.refresh_token
                user = response.user

                # Retornar los datos de autenticación
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user
                }
            else:
                # Si no hay sesión, entonces las credenciales son incorrectas
                logging.error("Credenciales incorrectas.")
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        except Exception as e:
            logging.error(f"Error en el servidor al intentar iniciar sesión: {str(e)}")
            raise HTTPException(status_code=500, detail="Error en el servidor")
