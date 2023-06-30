from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .config import get_config
from .api.v1 import router
from .api.auth import auth_router

app = FastAPI()
settings = get_config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def app_init():
    db_client = AsyncIOMotorClient(settings.mongo_uri).NoSQLTodo
    await init_beanie(
        database=db_client,
        document_models=[
            'app.models.user.UserModel',
            'app.models.todo.TodoModel',
            'app.models.sharedtodo.SharedTodoModel'
        ]
    )


app.include_router(router, prefix='/api/v1')
app.include_router(auth_router, prefix='/auth', tags=['auth'])

# To-Do: Add Frontend