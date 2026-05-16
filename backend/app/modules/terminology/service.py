from app.core.supabase_client import supabase
from app.modules.terminology.constants import CODE_SYSTEMS


def search_codes(system: str, query: str):
    if system not in CODE_SYSTEMS:
        raise ValueError("Unsupported code system")

    response = (
        supabase
        .table("terminology_codes")
        .select("system, code, display")
        .eq("system", system)
        .ilike("display", f"%{query}%")
        .limit(20)
        .execute()
    )

    return [
        {
            "system": CODE_SYSTEMS[row["system"]],
            "code": row["code"],
            "display": row["display"]
        }
        for row in response.data
    ]
