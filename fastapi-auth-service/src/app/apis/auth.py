from fastapi import APIRouter, Depends, HTTPException, status
from app.shemas.auth import LoginRequest, TokenResponse
from app.service.auth_service import AuthService, get_auth_service
from app.utils.auth import oauth2_scheme

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
async def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
    token = auth_service.create_user_token(user)
    return token

@router.post("/logout",
             status_code=status.HTTP_204_NO_CONTENT,
             description="User logout endpoint",
             responses={
                 401: {"description": "Invalid token"}
             })
async def logout(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    auth_service.logout_user(token)
    return
