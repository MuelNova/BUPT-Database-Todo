from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from uuid import UUID

from ... import get_current_user
from ....models import UserModel
from ....schemas import ListTodoResponse, TodoCreate, TodoResponse, TodoUpdate
from ....services import TodoService

todo_router = APIRouter()


@todo_router.get('/', summary="Get All To-Do of Current User", response_model=ListTodoResponse)
async def _(user: UserModel = Depends(get_current_user)):
    todos = await TodoService.get_todos(user)
    return ListTodoResponse(todos=todos, count=len(todos))


@todo_router.post('/', summary="Create a new To-Do", response_model=TodoResponse)
async def _(data: TodoCreate, user: UserModel = Depends(get_current_user)):
    return await TodoService.create_todo(user, data)

@todo_router.get('/{todo_id}', summary="Get a To-Do from Current User", response_model=TodoResponse)
async def _(todo_id: UUID, user: UserModel = Depends(get_current_user)):
    todo = await TodoService.get_todo_by_id(todo_id)
    if todo.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this To-Do")
    return TodoResponse(**todo.dict())

@todo_router.patch('/{todo_id}', summary="Update a To-Do", response_model=TodoResponse)
async def _(todo_id: UUID, data: TodoUpdate, user: UserModel = Depends(get_current_user)):
    todo = await TodoService.get_todo_by_id(todo_id)
    if todo.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this To-Do")
    return await TodoService.update_todo(todo, data)

@todo_router.delete('/{todo_id}', summary="Delete a To-Do", response_model=TodoResponse)
async def _(todo_id: UUID, user: UserModel = Depends(get_current_user)):
    todo = await TodoService.get_todo_by_id(todo_id)
    if todo.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this To-Do")
    await TodoService.delete_todo(todo)
    return todo
