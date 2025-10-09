from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.authentication import UnauthenticatedUser, AuthCredentials
from app.database import SessionLocal

from app.models.user import User
from app.utils.auth import SECRET_KEY, ALGORITHM
from app.utils.redis import get_email_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class JWTAuthBackend:
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return

            # Check if token is in Redis
            if get_email_by_token(token) is None:
                return

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return
        except (ValueError, JWTError):
            # Token is invalid
            return

        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if user is None:
            return

        return AuthCredentials(["authenticated"]), user
