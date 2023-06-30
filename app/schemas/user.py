from uuid import UUID
from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    username: str = Field(..., min_length=1, max_length=25, description="user username")
    password: str = Field(..., min_length=5, max_length=25, description="user password")


class UserResponse(BaseModel):
    user_id: UUID
    username: str


class UserName(BaseModel):
    username: str = Field(..., min_length=1, max_length=25, description="user username")