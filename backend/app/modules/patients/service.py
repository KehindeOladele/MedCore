from app.core.supabase_client import supabase

#     ----- Get or Create Patient Service -----
def get_or_create_patient(user_id: str):
    response = (
        supabase
        .table("patients")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    insert = (
        supabase
        .table("patients")
        .insert({
            "id": user_id,
            "fhir_metadata": {
                "resourceType": "Patient"
            }
        })
        .execute()
    )

    return insert.data[0]

#      ----- Old Implementation -----
# def get_or_create_patient(user_id: str):
#     """
#     Fetch patient row for authenticated user.
#     Auto-create if missing.
#     """

#     response = (
#         supabase
#         .table("patients")
#         .select("*")
#         .eq("id", user_id)
#         .execute()
#     )

#     if response.data:
#         return response.data[0]

#     # Auto-create patient row
#     insert = (
#         supabase
#         .table("patients")
#         .insert({"id": user_id})
#         .execute()
#     )

#     return insert.data[0]
