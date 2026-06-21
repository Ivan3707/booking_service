from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from src.auth.jwt import decode_token

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):
    token = credentials.credentials

    try:
        payload = decode_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def require_user(user=Depends(get_current_user)):

    if user["role"] != "user":

        raise HTTPException(status_code=403, detail="Users only")

    return user

def require_admin(user=Depends(get_current_user)):

    if user["role"] != "admin":

        raise HTTPException(status_code=403, detail="Admins only")

    return user