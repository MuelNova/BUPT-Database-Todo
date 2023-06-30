from fastapi import APIRouter

from .handlers import user_router, todo_router, shared_todo_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['user'])
router.include_router(todo_router, prefix='/todo', tags=['todo'])
router.include_router(shared_todo_router, prefix='/todo/share', tags=['shared todo'])