from app.config import settings
from app.database.supabase import get_supabase_client
from app.schemas.api import SettingsOut, SettingsUpdate, SettingsResponse

MOCK_SETTINGS = {
    "id": "set-001",
    "name": "Nexora University",
    "tagline": "Where Innovation Meets Excellence",
    "description": "Empowering Innovation, Inspiring Future Leaders through quality education, research, and industry collaboration.",
    "vision": "To create a next-generation digital university ecosystem that makes education and information seamless, interactive, and accessible globally.",
    "mission": "Deliver world-class education, foster cutting-edge research, and empower student growth.",
    "email": "info@nexorauniversity.edu",
    "phone": "+91 98765 43210",
    "address": "Nexora Campus, Innovation District, Hyderabad, Telangana 500032",
    "logo_url": "/assets/logo.png",
    "banner_url": "/assets/banner.jpg",
    "social_links": {
        "facebook": "https://facebook.com/nexorauniversity",
        "twitter": "https://twitter.com/nexorauniversity",
        "linkedin": "https://linkedin.com/school/nexorauniversity",
        "instagram": "https://instagram.com/nexorauniversity",
    },
    "updated_at": "2026-01-01T00:00:00Z",
}


class SettingsService:
    """Service handling university settings read and update operations."""

    @staticmethod
    def get_settings() -> SettingsResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        if not is_placeholder:
            try:
                res = supabase.table("university_settings").select("*").limit(1).execute()
                if res.data and len(res.data) > 0:
                    return SettingsResponse(
                        message="University settings fetched successfully",
                        status="success",
                        data=SettingsOut(**res.data[0]),
                    )
            except Exception:
                pass

        return SettingsResponse(
            message="University settings fetched successfully (Development Mode)",
            status="success",
            data=SettingsOut(**MOCK_SETTINGS),
        )

    @staticmethod
    def update_settings(payload: SettingsUpdate) -> SettingsResponse:
        supabase = get_supabase_client()
        is_placeholder = settings.supabase_url == "https://your-project.supabase.co"

        updates = {k: v for k, v in payload.model_dump().items() if v is not None}

        if not is_placeholder:
            try:
                # Check if settings row exists
                res = supabase.table("university_settings").select("id").limit(1).execute()
                if res.data and len(res.data) > 0:
                    setting_id = res.data[0]["id"]
                    updated = supabase.table("university_settings").update(updates).eq("id", setting_id).execute()
                    if updated.data:
                        return SettingsResponse(
                            message="University settings updated successfully",
                            status="success",
                            data=SettingsOut(**updated.data[0]),
                        )
                else:
                    inserted = supabase.table("university_settings").insert(updates).execute()
                    if inserted.data:
                        return SettingsResponse(
                            message="University settings initialized and saved",
                            status="success",
                            data=SettingsOut(**inserted.data[0]),
                        )
            except Exception as err:
                if settings.environment != "development":
                    raise err

        MOCK_SETTINGS.update(updates)
        return SettingsResponse(
            message="University settings updated successfully (Development Mode)",
            status="success",
            data=SettingsOut(**MOCK_SETTINGS),
        )
