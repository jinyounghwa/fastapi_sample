from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.shemas.auth import LoginRequest, TokenResponse

router = APIRouter()
@router.post("/login",
             response_model=TokenResponse,
             description="User login endpoint",
             responses={
                 401: {"description": "Invalid credentials",
                       "content": {
                           "application/json": {
                               "example": {"detail": "Invalid email or password"}
                           }
                       }
                 },
             })
async def login(request: LoginReques, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
    token = auth_service.create_user_token(user)
    return token

