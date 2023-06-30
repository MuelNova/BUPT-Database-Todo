from uuid import UUID
from typing import List, Generator

from ..models import TodoModel, UserModel, SharedTodoModel
from ..schemas import TodoCreate, TodoUpdate, TodoSharedUpdate


class TodoService:

    @staticmethod
    async def get_todos(user: UserModel) -> List[TodoModel]:
        todos = await TodoModel.find(TodoModel.owner.id == user.id).to_list()
        return todos
    
    @staticmethod
    async def get_all_shared_todos(user: UserModel) -> List[List[SharedTodoModel]]:
        return [await TodoService.get_shared_todos(user), await TodoService.get_shared_todos_received(user)]
    
    @staticmethod
    async def get_shared_todos(user: UserModel) -> List[SharedTodoModel]:
        return await SharedTodoModel.find(SharedTodoModel.owner.id == user.id, fetch_links=True).to_list()
    
    @staticmethod
    async def get_shared_todos_received(user: UserModel) -> List[SharedTodoModel]:
        return await SharedTodoModel.find(SharedTodoModel.shared_with.id == user.id, fetch_links=True).to_list()

    @staticmethod
    async def create_todo(user: UserModel, data: TodoCreate) -> TodoModel:
        todo = TodoModel(**data.dict(), owner=user)
        return await todo.insert()

    @staticmethod
    async def update_todo(todo: TodoModel, data: TodoUpdate) -> TodoModel:
        await todo.set(data.dict(exclude_unset=True))
        return todo
        

    @staticmethod
    async def delete_todo(todo: TodoModel):
        shared_todos = await TodoService.get_shared_todos_by_todo(todo)
        for shared_todo in shared_todos:
            await TodoService.revoke_shared_todo(shared_todo)  # revoke shared todos at the same time.
        await todo.delete()

    @staticmethod
    async def share_todo(owner: UserModel, todo: TodoModel, shared_with: UserModel) -> SharedTodoModel:
        shared_todo = SharedTodoModel(owner=owner, todo=todo, shared_with=shared_with)
        todo.shared_with.append(shared_with.username)
        shared_todo.todo = await TodoService.update_todo(todo, TodoSharedUpdate(shared_with=todo.shared_with))
        await shared_todo.insert()
        return shared_todo
    
    @staticmethod
    async def revoke_shared_todo(shared_todo: SharedTodoModel) -> SharedTodoModel:
        shareds = shared_todo.todo.shared_with
        shareds.remove(shared_todo.shared_with.username)
        await TodoService.update_todo(shared_todo.todo, TodoSharedUpdate(shared_with=shareds))
        await shared_todo.delete()
        return shared_todo

    @staticmethod
    async def get_todo_by_id(todo_id: UUID) -> TodoModel:
        todo = await TodoModel.find_one(TodoModel.todo_id == todo_id, fetch_links=True)
        return todo
    
    @staticmethod
    async def get_shared_todos_by_id(todo_id: UUID) -> List[SharedTodoModel]:
        return await SharedTodoModel.find(SharedTodoModel.todo.todo_id == todo_id, fetch_links=True).to_list()
    
    @staticmethod
    async def get_shared_todos_by_todo(todo: TodoModel) -> List[SharedTodoModel]:
        return await SharedTodoModel.find(SharedTodoModel.todo.id == todo.id, fetch_links=True).to_list()
    
    @staticmethod
    async def get_shared_todo_by_todo_and_user(todo: TodoModel, user: UserModel) -> SharedTodoModel:
        return await SharedTodoModel.find_one(SharedTodoModel.todo.id == todo.id,
                                              SharedTodoModel.shared_with.id == user.id,
                                              fetch_links=True)
