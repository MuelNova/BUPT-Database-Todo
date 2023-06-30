from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field


class UserModel(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    hashed_password: str

    def __repr__(self) -> str:
        return f"<User id={self.user_id}, username={self.username}, hashed_password={self.hashed_password}>"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.username)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserModel):
            return self.username == other.username
        return False


    class Settings:
        name = 'users'