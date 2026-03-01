import jwt
from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.utils.auth import create_access_token
from app.utils.response import api_response
from database import get_db
from app.utils.settings import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
security = HTTPBearer()


# async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
#     try:
#         payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

#         user_id = payload.get("_id")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")

#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalars().first()

#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user

# ? verify jwt token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        user_id = payload.get("_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user




