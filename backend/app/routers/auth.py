from fastapi import APIRouter, HTTPException
from Schemas.Auth import LoginRequest, UpdatePasswordRequest
from controllers.auth_controller import AuthController
import logging

auth_router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={404: {"message": "No encontrado"}}
)

auth_controller = AuthController()

@auth_router.post("/login")
async def login(request: LoginRequest):
    logging.info(f"Solicitud de login recibida para el correo: {request.email}")
    try:
        response = auth_controller.iniciar_sesion(request.email, request.password)
        logging.info("Login exitoso")
        return response
    except HTTPException as e:
        logging.error(f"Error en el login: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"Error en el servidor: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
@auth_router.post("/update-password")
async def update_password(request: UpdatePasswordRequest):
    return auth_controller.actualizar_password(request)