from typing import Optional
from passlib.context import CryptContext
from uuid import UUID

from ..schemas import UserAuth
from ..models import UserModel

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    @staticmethod
    async def create_user(user: UserAuth) -> UserModel:
        user = UserModel(username=user.username, hashed_password=UserService.get_hashed_password(user.password))
        await user.save()
        return user
    
    @staticmethod
    async def authenticate(user: UserAuth) -> Optional[UserModel]:
        user_ = await UserService.get_user_by_username(user.username)
        if not user_:
            return None
        if not UserService.verify_password(user.password, user_.hashed_password):
            return None
        return user_
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[UserModel]:
        return await UserModel.find_one(UserModel.username == username)
    
    @staticmethod
    async def get_user_by_ID(ID: UUID) -> Optional[UserModel]:
        return await UserModel.find_one(UserModel.user_id == ID)
    