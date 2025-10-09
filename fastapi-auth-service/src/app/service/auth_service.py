from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select
from app.utils.security import verify_password
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
 

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    def authenticate_user(self, email: str, password: str):
        query = (
            select(User).where(User.email == email)
        )
        user = self.db.execute(query).scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user_token(self, user: User):
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "is_active": user.is_active
        }
        access_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    def get_auth_service(db: Session = None):
        return AuthService(db)
