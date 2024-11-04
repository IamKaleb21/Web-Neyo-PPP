# routers/auth.py
from fastapi import APIRouter
from Schemas.Auth import LoginRequest
from controllers.auth_controller import AuthController

# Configuración del router de autenticación
auth = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={404: {"message": "No encontrado"}}
)

# Instancia del controlador de autenticación
auth_controller = AuthController()

@auth.post("/login")
def login(request: LoginRequest):
    return auth_controller.iniciar_sesion(request.email, request.password)
