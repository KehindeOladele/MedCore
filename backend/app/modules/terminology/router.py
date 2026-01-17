from fastapi import APIRouter, Query
from app.modules.terminology.service import search_codes

router = APIRouter(prefix="/terminology", tags=["Terminology"])


@router.get("/{system}")
def lookup_codes(system: str, q: str = Query(..., min_length=2)):
    return search_codes(system.upper(), q)
