from fastapi import HTTPException
from pwdlib import PasswordHash
import jwt
from app.utils.response import api_response
from app.utils.settings import settings
from datetime import datetime,timedelta


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data:dict)->str:
    
    payload = data.copy()
    payload["type"] = "access"
    payload["exp"] = datetime.utcnow() + timedelta(minutes=settings.EXP_TIME)
    
    # jwt.encode(payload,secretKey,Algo)
    token = jwt.encode(payload,settings.SECRET_KEY,settings.ALGORITHM)
    
    return token

def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    payload["type"] = "refresh"
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


async def regenrate_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("_id")

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token({"_id": user_id})

        return api_response(
            status_code=200,
            message="Token refreshed",
            data={"access_token": new_access_token}
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
