from pydantic import BaseModel, Field , EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username:str = Field(min_length=2)
    email : EmailStr = Field(min_length=5)


class UserCreate(UserBase):
    password : str = Field(min_length=3)


class UserReponse(UserBase):
    id:int
    created_at : datetime

class LoginSchema(BaseModel):
    username : str = Field(..., min_length=2)
    password : str = Field(...,min_length=5)

class OTPVerifySchema(BaseModel):
    email : EmailStr = Field(..., min_length=5)
    otp : str = Field(..., min_length=4, max_length=6)