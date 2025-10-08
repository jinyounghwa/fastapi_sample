from fastapi import APIRouter, Depends, HTTPException
from app.shemas.user import UserCreate, UserResponse
from app.service.user_service import UserService, get_user_service

router = APIRouter()

@router.post("/register",
             response_model=UserResponse,
             description="Register a new user",
             summary="User Registration",
             responses={
                 409:{"description":"User already exists",
                       "content":{"application/json":{"example":{"detail":"User with this email or username already exists"}}}
             }
                }
             )
def register_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    existing_user = user_service.get_user_by_email(user.email) or user_service.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email or username already exists")
    created_user = user_service.crate_user(user)
    return created_user