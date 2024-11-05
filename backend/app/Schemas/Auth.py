# Schemas/Auth.py
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class UpdatePasswordRequest(BaseModel):
    acces_token: str  # Asegúrate de que este nombre coincida
    new_password: str