from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from pydantic import ValidationError
from jose import jwt, JWTError

from .. import get_current_user, create_access_token, create_refresh_token
from ...config import get_config
from ...services import UserService
from ...schemas import TokenResponse, TokenPayload, UserResponse, UserAuth


settings = get_config()
auth_router = APIRouter()


@auth_router.post('/login', summary="Create access and refresh token", response_model=TokenResponse)
async def _(login: OAuth2PasswordRequestForm = Depends()):
    user = await UserService.authenticate(UserAuth(username=login.username, password=login.password))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect username or password")

    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }


@auth_router.post('/validate', summary="Test if the access token is vaild", response_model=UserResponse)
async def _(user: str = Depends(get_current_user)):
    return user


@auth_router.post('/refresh', summary="Use refresh token to get a new access token", response_model=TokenResponse)
async def _(refresh_token:str = Body(...)):
    try:
        payload = jwt.decode(refresh_token, settings.jwt_refresh_secret_key, algorithms="HS256")
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired",
                                headers={"WWW-Authenticate": "Bearer"})
    except(JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    user = await UserService.get_user_by_ID(token_data.sub)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find the user")

    return {
        "access_token":create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }
    
