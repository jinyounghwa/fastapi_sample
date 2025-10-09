from sqlalchemy.orm import Session
from app.models import User
from sqlalchemy import select
from app.utils.security import verify_password
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.database import get_db
from fastapi import Depends
from app.utils.redis import set_token, delete_token

class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def authenticate_user(self, email: str, password: str):
        query = select(User).where(User.email == email)
        user = self.db.execute(query).scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user_token(self, user: User):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires,
        )
        set_token(access_token, user.email, int(access_token_expires.total_seconds()))
        return {"access_token": access_token, "token_type": "bearer"}

    def logout_user(self, token: str):
        delete_token(token)

def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)
