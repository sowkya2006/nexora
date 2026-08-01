from fastapi import APIRouter
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse, PasswordResetRequest, PasswordResetResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest):
    """Admin login via Supabase Auth."""
    return AuthService.login(body)


@router.post("/logout", response_model=LogoutResponse)
async def logout():
    """Admin logout via Supabase Auth."""
    return AuthService.logout()


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password(body: PasswordResetRequest):
    """Admin password reset email request."""
    return AuthService.reset_password(body.email)
