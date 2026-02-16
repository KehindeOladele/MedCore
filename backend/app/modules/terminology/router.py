from fastapi import APIRouter, Query, HTTPException
from app.modules.terminology.service import search_codes
from app.modules.terminology.constants import CODE_SYSTEMS

router = APIRouter(prefix="/terminology", tags=["Terminology"])


@router.get("/{system}")
def lookup_codes(
    system: str,
    q: str = Query(..., min_length=2)
):
    system = system.upper()

    if system not in CODE_SYSTEMS:
        raise HTTPException(status_code=400, detail="Unsupported terminology system")

    return search_codes(system, q)
