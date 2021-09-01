from pydantic import BaseModel
from typing import List


class BasePost(BaseModel):
    title: str
    body: str


class SavePost(BasePost):
    user_id: int


class BaseLike(BaseModel):
    user_id: int


class ShowPost(BasePost):
    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(BaseUser):
    posts: List[ShowPost] = []
    liked_posts: List[ShowPost] = []

    class Config:
        orm_mode = True

