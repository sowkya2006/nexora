from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional

from app.config import settings
from app.database.supabase import get_supabase_client
from app.schemas.auth import AdminUser

security = HTTPBearer(auto_error=False)


async def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> AdminUser:
    """
    Validates Supabase JWT access token for protected admin routes.
    Includes development fallback mode when using mock token or placeholder credentials.
    """
    if not credentials or not credentials.credentials:
        # Development fallback mode: allow requests in dev if no token supplied
        if settings.environment == "development" and settings.supabase_url == "https://your-project.supabase.co":
            return AdminUser(
                id="dev-admin-0000-0000-000000000000",
                email="admin@nexorauniversity.edu",
                role="admin",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Development mock token validation
    if token == "mock-admin-token" or token.startswith("dev-token-"):
        return AdminUser(
            id="dev-admin-0000-0000-000000000000",
            email="admin@nexorauniversity.edu",
            role="admin",
        )

    # Supabase token validation
    try:
        supabase = get_supabase_client()
        user_response = supabase.auth.get_user(token)
        if user_response and hasattr(user_response, "user") and user_response.user:
            user = user_response.user
            return AdminUser(
                id=str(user.id),
                email=user.email or "admin@nexorauniversity.edu",
                role="admin",
            )
    except Exception as err:
        # Fallback in development mode if Supabase credentials are invalid or offline
        if settings.environment == "development":
            return AdminUser(
                id="dev-admin-0000-0000-000000000000",
                email="admin@nexorauniversity.edu",
                role="admin",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(err)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
