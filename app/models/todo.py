from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional, List
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import Field

from .user import UserModel

class TodoStatus(Enum):
    PENDING = 1
    WORKING = 2
    DONE = 3


class TodoModel(Document):
    todo_id: UUID = Field(default_factory=uuid4, unique=True)
    status: TodoStatus = Field(default=TodoStatus.PENDING, repr=lambda x: x.value)
    title: Indexed(str)
    description: str
    sub_tasks: Optional[List[str]] = []
    shared_with: Optional[List[str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Link[UserModel]

    def __repr__(self) -> str:
        return f"<Todo id={self.todo_id}, title={self.title}, description={self.description}" \
               f"status={self.status}, created_at={self.created_at}, updated_at={self.updated_at}, owner={self.owner.username}" \
               f", shared_with={self.shared_with}>"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TodoModel):
            return self.todo_id == other.todo_id
        return False

    @before_event(Replace, Insert)
    def update_update_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "todos"
