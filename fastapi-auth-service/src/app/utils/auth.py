from datetime import datetime, timedelta
from typing import Optional
from jose import jwt


SECRET_KEY = "12123131231312313131312"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict, exprires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if exprires_delta:
        expire = datetime.utcnow() + exprires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

def verify_token(token:str)->dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None


    
    