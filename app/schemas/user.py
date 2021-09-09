from pydantic import BaseModel
from typing import List
from schemas import post


class BaseUser(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class BaseUserWithPass(BaseUser):
    password: str


class ShowUser(BaseUser):
    posts: List[post.ShowPost] = []
    # liked_posts: List[post.ShowPost] = []

    class Config:
        orm_mode = True
