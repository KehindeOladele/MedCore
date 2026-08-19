from app.core.supabase_client import supabase

#  ----- lookup query -----
def search_codes(system: str, q: str):
    """"
    looks-up codes and systems using representative name like eg. malaria and gives the specification standards.

    input str: popular name of disease, drug etc.
    return str: display name, code, and system.
    """
    response = (
        supabase
        .table("terminology_codes")
        .select("*")
        .eq("system", system)
        .ilike("display", f"%{q}%")
        .limit(10)
        .execute()
    )
    return response.data