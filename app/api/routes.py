from __future__ import annotations
from fastapi import APIRouter, Depends
from ..services.synonyms import SynonymService

router = APIRouter()

def get_service() -> SynonymService:
    from ..main import container  # simple service locator
    return container["syn_service"]

@router.get("/synonyms")
async def list_synonyms(svc: SynonymService = Depends(get_service)):
    result = await svc.get_all()
    return {"cached": result["source"] == "cache", "data": result["items"]}

@router.post("/cache/invalidate")
async def invalidate_cache(svc: SynonymService = Depends(get_service)):
    await svc.invalidate()
    return {"ok": True}
