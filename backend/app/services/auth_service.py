from typing import Dict, Any
from app.config import settings
from app.database.supabase import get_supabase_client
from app.schemas.auth import LoginRequest, LoginResponse, AdminUser, LogoutResponse, PasswordResetResponse


class AuthService:
    """Service handling Admin authentication operations using Supabase Auth with dev fallback."""

    @staticmethod
    def login(payload: LoginRequest) -> LoginResponse:
        supabase = get_supabase_client()
        
        # Check if environment is using placeholder credentials or dev credentials
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"
        
        if not is_placeholder:
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": payload.email,
                    "password": payload.password,
                })
                if res and res.session and res.user:
                    user_data = AdminUser(
                        id=str(res.user.id),
                        email=res.user.email or payload.email,
                        role="admin",
                    )
                    return LoginResponse(
                        message="Admin login successful",
                        status="success",
                        access_token=res.session.access_token,
                        token_type="bearer",
                        user=user_data,
                    )
            except Exception as err:
                # If real login fails and not in dev fallback, raise or let fallback catch if admin test
                if settings.environment != "development":
                    raise err

        # Development Fallback Mode
        user_data = AdminUser(
            id="dev-admin-0000-0000-000000000000",
            email=payload.email,
            role="admin",
        )
        return LoginResponse(
            message="Admin login successful (Development Mode)",
            status="success",
            access_token="dev-token-admin-session-xyz",
            token_type="bearer",
            user=user_data,
        )

    @staticmethod
    def logout() -> LogoutResponse:
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
        except Exception:
            pass  # Fail-safe in case of offline/mock session
        return LogoutResponse(message="Successfully logged out", status="success")

    @staticmethod
    def reset_password(email: str) -> PasswordResetResponse:
        try:
            supabase = get_supabase_client()
            supabase.auth.reset_password_email(email)
        except Exception:
            pass
        return PasswordResetResponse(
            message=f"Password reset link sent to {email} if the account exists",
            status="success",
        )
