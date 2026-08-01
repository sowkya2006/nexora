from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminUser(BaseModel):
    id: str
    email: str
    role: str = "admin"
    created_at: Optional[str] = None


class LoginResponse(BaseModel):
    message: str
    status: str = "success"
    access_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[AdminUser] = None


class LogoutResponse(BaseModel):
    message: str
    status: str = "success"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    message: str
    status: str = "success"
