from pydantic import BaseModel
from pydantic import Field

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id:int
    created_at: str
    class Config:
        from_attributes = True
        
