from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_admin
from app.schemas.api import SettingsUpdate, SettingsResponse
from app.schemas.auth import AdminUser
from app.services.settings_service import SettingsService

router = APIRouter()


@router.get("/", response_model=SettingsResponse)
async def get_settings():
    """Get university settings."""
    return SettingsService.get_settings()


@router.put("/", response_model=SettingsResponse)
async def update_settings(
    payload: SettingsUpdate,
    _admin: AdminUser = Depends(get_current_admin),
):
    """Update university settings (Admin only)."""
    return SettingsService.update_settings(payload)
