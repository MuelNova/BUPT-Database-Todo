from time import sleep
from beanie import init_beanie
from beanie.exceptions import RevisionIdWasChanged
from motor.motor_asyncio import AsyncIOMotorClient


from app.models import SharedTodoModel
from app.services import TodoService, UserService
from app.schemas import UserAuth
from app.schemas import TodoCreate


async def app_init():
    db_client = AsyncIOMotorClient("mongodb://localhost:27017").NoSQLTodo
    await init_beanie(
        database=db_client,
        document_models=[
            'app.models.user.UserModel',
            'app.models.todo.TodoModel', 
            'app.models.sharedtodo.SharedTodoModel'
        ]
    )
    
    try:
        await UserService.create_user(UserAuth(username='A', password='AAAAAA'))
        
    except RevisionIdWasChanged:
        print('User A already exists')

    try:
        await UserService.create_user(UserAuth(username='B', password='BBBBBB'))
        
    except RevisionIdWasChanged:
        print('User B already exists')

    try:
        await UserService.create_user(UserAuth(username='C', password='CCCCCC'))
    except RevisionIdWasChanged:
        print('User C already exists')

    user = await UserService.get_user_by_username('A')
    print(user)
    userB = await UserService.get_user_by_username('B')
    print(userB)
    userC = await UserService.get_user_by_username('C')
    print(userC)

    todos = []

    for u in range(10):
        todo = await TodoService.create_todo(user, TodoCreate(title=f'Test{u}', description=f'Test{u*u}'))
        todos.append(todo)

        shared_todo = await TodoService.share_todo(user, todo, userB)
        print(shared_todo)
        shared_todo = await TodoService.share_todo(user, todo, userC)
        print(shared_todo)
        # shared_todos_A = await TodoService.get_shared_todos(user)
        # print(shared_todos_A)

        # print(shared_todos_A[0])
    # for todo in todos:
    #     await TodoService.delete_todo(todo)
    # shared_todos_A = await TodoService.get_shared_todos(user)
    # print(shared_todos_A)
    
if __name__ == '__main__':
    import asyncio
    asyncio.run(app_init())