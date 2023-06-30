from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID

from ....schemas import ListTodoResponse, TodoSharedResponse, ListTodoSharedResponse, TodoResponse, UserName
from ....services import TodoService, UserService
from ....models import UserModel
from ... import get_current_user

shared_todo_router = APIRouter()

@shared_todo_router.get('/', summary="Get All Shared To-Do of Current User", response_model=ListTodoSharedResponse)
async def _(user: UserModel = Depends(get_current_user)):
    shared_todos = await TodoService.get_shared_todos(user)
    shared_todos = [TodoSharedResponse(**TodoResponse(**todo.todo.dict()).dict(exclude={'shared_with'}),
                                       owner=todo.owner.username,
                                       shared_with=todo.shared_with.username) for todo in shared_todos]
    return ListTodoResponse(todos=shared_todos, count=len(shared_todos))

@shared_todo_router.get('/received', summary="Get All Shared To-Do Received by Current User", response_model=ListTodoSharedResponse)
async def _(user: UserModel = Depends(get_current_user)):
    shared_todos = await TodoService.get_shared_todos_received(user)
    shared_todos = [TodoSharedResponse(**TodoResponse(**todo.todo.dict()).dict(exclude={'shared_with'}),
                                       owner=todo.owner.username,
                                       shared_with=todo.shared_with.username) for todo in shared_todos]
    return ListTodoResponse(todos=shared_todos, count=len(shared_todos))

@shared_todo_router.post('/{todo_id}', summary="Share a To-Do", response_model=TodoSharedResponse)
async def _(todo_id: UUID, shared_with: UserName, user: UserModel = Depends(get_current_user)):
    todo = await TodoService.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do not found")
    if todo.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this To-Do")
    shared_user = await UserService.get_user_by_username(shared_with.username)
    if shared_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sharing user not found")
    if shared_user.username in todo.shared_with:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="To-Do already shared with this user")
    if shared_user.id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot share a To-Do with yourself")
    result = await TodoService.share_todo(user, todo, shared_user)
    return TodoSharedResponse(**TodoResponse(**result.todo.dict()).dict(exclude={'shared_with'}),
                              owner=result.owner.username,
                              shared_with=result.shared_with.username)


@shared_todo_router.delete('/{todo_id}', summary="Unshare a To-Do", response_model=TodoResponse)
async def _(todo_id: UUID, shared_with: UserName, user: UserModel = Depends(get_current_user)):
    todo = await TodoService.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do not found")
    if todo.owner.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this To-Do")
    shared_user = await UserService.get_user_by_username(shared_with.username)
    if shared_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sharing user not found")
    shared_todo = await TodoService.get_shared_todo_by_todo_and_user(todo, shared_user)
    if shared_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do not shared with this user")
    result = await TodoService.revoke_shared_todo(shared_todo)
    return TodoResponse(**result.todo.dict())


@shared_todo_router.get('/{todo_id}', summary="Get a Shared To-Do", response_model=TodoSharedResponse)
async def _(todo_id: UUID, user: UserModel = Depends(get_current_user)):
    todo = await TodoService.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do not found")
    if todo.owner.id != user.id and todo.shared_with.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this To-Do")
    return TodoSharedResponse(**TodoResponse(**todo.dict()).dict(exclude={'shared_with'}),
                              owner=todo.owner.username,
                              shared_with=todo.shared_with.username)
