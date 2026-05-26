from app.core.supabase_admin import supabase_admin


# Create and Insert Medical_id to existing user
def generate_medical_id():

    result = (
        supabase_admin
        .table("patients")
        .select("*", count="exact")
        .execute()
    )

    next_number = (result.count or 0) + 1

    return f"MC-NG-{next_number:08d}"