from fastapi import APIRouter, HTTPException, status, Depends
from beanie.exceptions import RevisionIdWasChanged
from typing import List

from ....schemas import UserResponse, UserAuth
from ....services import UserService

user_router = APIRouter()


@user_router.post('/create', summary="Create a new user", response_model=UserResponse)
async def _(user: UserAuth):
    try:
        return await UserService.create_user(user)
    except RevisionIdWasChanged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Username already exists')

