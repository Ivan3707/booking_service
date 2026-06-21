from fastapi import APIRouter, HTTPException
from uuid import uuid4
from .jwt import create_access_token

router = APIRouter()

ADMIN_ID = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"


@router.post("/dummyLogin")
async def dummy_login(role: str):
    if role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="invalid role")

    user_id = ADMIN_ID if role == "admin" else USER_ID

    token = create_access_token({
        "user_id": user_id,
        "role": role
    })

    return {"access_token": token}
