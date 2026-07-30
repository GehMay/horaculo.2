from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum, StatusEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    status: StatusEnum
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: RoleEnum
    status: StatusEnum
