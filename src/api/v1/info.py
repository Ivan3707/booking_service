from fastapi import APIRouter

router = APIRouter()

@router.get("/_info")
async def info():
    return {"status": "ok"}