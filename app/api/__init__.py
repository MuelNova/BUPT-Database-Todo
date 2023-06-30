from datetime import datetime, timedelta
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from ..config import get_config
from ..models import UserModel
from ..services import UserService


settings = get_config()

async def get_current_user(token: str = Depends(OAuth2PasswordBearer('/auth/login', 'JWT'))) -> UserModel:
    try:
        user = await UserService.get_user_by_ID(UUID(jwt.decode(token, settings.jwt_secret_key, algorithms="HS256")['sub']))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find the user")
        return user
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    

def create_access_token(user_id: UUID, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode = {"exp": expire.timestamp(), "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm='HS256')
    return encoded_jwt


def create_refresh_token(user_id: UUID, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.jwt_refresh_token_expire_minutes)
    to_encode = {"exp": expire.timestamp(), "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret_key, algorithm='HS256')
    return encoded_jwt
