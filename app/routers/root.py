from fastapi import APIRouter
from . import login, posts, users

root_router = APIRouter()

root_router.include_router(login.router, prefix="/auth", tags=["auth"])
root_router.include_router(users.router, prefix="/users", tags=["users"])
root_router.include_router(posts.router, prefix="/posts", tags=["posts"])
