import os
import sys
from app.config import settings
from app.database.supabase import get_supabase_client

print("==========================================================================")
print("CREATING / VERIFYING SUPABASE ADMIN USER")
print("==========================================================================")

supabase = get_supabase_client()

admin_email = "admin@nexora.edu"
admin_password = "Admin@123456"

try:
    # Use admin service role to create user with email_confirm=True (bypasses email confirmation requirement)
    user_res = supabase.auth.admin.create_user({
        "email": admin_email,
        "password": admin_password,
        "email_confirm": True,
        "user_metadata": {"role": "admin", "full_name": "Administrator"}
    })
    print(f"[OK] Admin user '{admin_email}' created successfully in Supabase Auth! (Email confirmation bypassed)")
except Exception as e:
    print(f"[NOTE] Admin user creation note: {e}")
    # Try updating existing user password to ensure Admin@123456 works
    try:
        users = supabase.auth.admin.list_users()
        admin_u = next((u for u in users if u.email == admin_email), None)
        if admin_u:
            supabase.auth.admin.update_user_by_id(admin_u.id, {"password": admin_password, "email_confirm": True})
            print(f"[OK] Admin user '{admin_email}' password updated & email confirmed!")
    except Exception as err2:
        print(f"[NOTE] Admin update note: {err2}")

# Test sign_in_with_password
try:
    auth_res = supabase.auth.sign_in_with_password({
        "email": admin_email,
        "password": admin_password
    })
    if auth_res and auth_res.session:
        print(f"[SUCCESS] Signed in successfully with '{admin_email}'! Access Token generated: {auth_res.session.access_token[:20]}...")
    else:
        print(f"[FAIL] Could not sign in with '{admin_email}'")
except Exception as err:
    print(f"[FAIL] Sign in test error: {err}")

print("==========================================================================")
