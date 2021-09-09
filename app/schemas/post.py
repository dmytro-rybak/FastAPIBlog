from pydantic import BaseModel


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
