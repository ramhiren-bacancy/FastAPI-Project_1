import json

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy import select
from typing_extensions import Annotated

from app.utils.redis_client import redis_client
from app.utils.otp_gen import generate_otp
from email_service import send_otp_email, send_welcome_email
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import LoginSchema, OTPVerifySchema, UserCreate, UserReponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import settings
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    regenrate_access_token,
    verify_password,
)
from app.utils.dependencies import get_current_user
from app.utils.error_decorator import db_exception_handler
from app.utils.response import api_response
from database import get_db


router = APIRouter()

# security = HTTPBearer()


@router.post(
    "/register",
    response_model=ApiResponse[UserReponse],
    status_code=status.HTTP_201_CREATED,
)
@db_exception_handler
async def user_register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    # ! if Don't check error here then decoder give error but with Genral error like "DB Error". it not give specific error
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username is Already Exits"
        )

    result = await session.execute(select(User).where(User.email == user.email))
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is Already Register"
        )

    otp = generate_otp()
    
    await redis_client.set(f"signup:otp:{user.email}", otp, ex=300)
    
    await redis_client.set(
        f"signup:data:{user.email}",
        user.model_dump_json(),
        ex=300,
    )
    
    background_tasks.add_task(send_otp_email, user.email, otp)
    
    return api_response(
        status_code=201, message="OTP sent successfully"
    )
    
    # new_user = User(
    #     username=user.username,
    #     password=get_password_hash(user.password),
    #     email=user.email,
    # )

    # session.add(new_user)
    # await session.commit()
    # await session.refresh(new_user)

    # background_tasks.add_task(send_welcome_email, new_user.email, new_user.username)

    # return api_response(
    #     status_code=201, message="User Create Successfully", data=new_user
    # )


@router.post("/verify-otp",response_model=ApiResponse[UserReponse], status_code=status.HTTP_201_CREATED)
async def verify_otp(
    data: OTPVerifySchema,
    session: AsyncSession = Depends(get_db),
):
    stored_otp = await redis_client.get(f"signup:otp:{data.email}")

    if not stored_otp:
        raise HTTPException(status_code=400, detail="OTP expired")

    if stored_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user_data = await redis_client.get(f"signup:data:{data.email}")

    if not user_data:
        raise HTTPException(status_code=400, detail="Session expired")

    user_dict = json.loads(user_data)

    new_user = User(
        username=user_dict["username"],
        email=user_dict["email"],
        password=get_password_hash(user_dict["password"]),
    )

    session.add(new_user)
    await session.commit()

    # cleanup
    await redis_client.delete(f"signup:otp:{data.email}")
    await redis_client.delete(f"signup:data:{data.email}")

    return api_response(
        status_code=201, message="User Create Successfully", data=new_user
    )









@router.post("/login", response_model=ApiResponse, status_code=status.HTTP_200_OK)
@db_exception_handler
# async def user_login( user: OAuth2PasswordRequestForm = Depends(),session: AsyncSession = Depends(get_db)):
# async def user_login(user: LoginSchema, session: AsyncSession = Depends(get_db)):
async def user_login(
    username: str, password: str, session: AsyncSession = Depends(get_db)
):
    # username = user.username
    # password = user.password
    result = await session.execute(select(User).where(User.username == username))
    exits_user = result.scalars().first()
    if not exits_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username Not Exits"
        )

    if not verify_password(password, exits_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Not Match"
        )

    token = create_access_token({"_id": exits_user.id})
    refresh_token = create_refresh_token({"_id": exits_user.id})

    data = {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

    response = api_response(status_code=200, message="Login successful", data=data)

    return response


@router.get("/me", response_model=ApiResponse[UserReponse])
async def read_me(current_user: User = Depends(get_current_user)):
    return api_response(
        status_code=200, message="User profile fetch successfully", data=current_user
    )


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    return await regenrate_access_token(refresh_token)
