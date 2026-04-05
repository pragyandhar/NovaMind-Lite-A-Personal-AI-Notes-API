# ---------------------------------------
# Hashing - Imports
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
def hash_password(password: str):
    hpass = pwd_context.hash(password)
    return hpass

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

# ---------------------------------------
# JWT Imports
import jwt 
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from app.config import settings

load_dotenv()
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"

def create_access_token(data: dict):
    user_id = data.get("sub")

    # Create a token
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=30)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature doesn't match"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token couldn't be decoded (malformed)"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Token: Missing Subject"
        )
    return user_id
    
