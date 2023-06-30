from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, validator

from app.models.todo import TodoStatus


class TodoCreate(BaseModel):
    title: str = Field(..., title="Title", max_length=55, min_length=1)
    description: str = Field(..., title="Description", max_length=7555, min_length=1)
    sub_tasks: List[str] = Field([], title="Sub Tasks", max_length=7555, min_length=0)
    status: TodoStatus = TodoStatus.PENDING
    

class TodoUpdate(BaseModel):
    title: str = Field(None, title="Title", max_length=55, min_length=1)
    description: str = Field(None, title="Description", max_length=7555, min_length=1)
    sub_tasks: List[str] = Field([], title="Sub Tasks", max_length=7555, min_length=0)
    status: TodoStatus = TodoStatus.PENDING

class TodoSharedUpdate(TodoUpdate):
    shared_with: List[str] = Field([], title="Shared With", max_length=7555, min_length=0)

class TodoResponse(BaseModel):
    todo_id: UUID
    title: str
    description: str
    sub_tasks: Optional[List[str]] = Field([], title="Sub Tasks", max_length=7555, min_length=0)
    status: TodoStatus = TodoStatus.PENDING
    shared_with: List[str] = []


class TodoSharedResponse(TodoResponse):
    owner: str
    shared_with: str


class ListTodoResponse(BaseModel):
    todos: List[TodoResponse]
    count: int


class ListTodoSharedResponse(BaseModel):
    todos: List[TodoSharedResponse]
    count: int
