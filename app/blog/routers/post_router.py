from fastapi import Depends, APIRouter, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from db.database import get_db
from blog import schemas
from blog.crud.post_crud import PostCRUD
from typing import List

post_router = APIRouter(tags=['Post'])


@cbv(post_router)
class Post:
    session: Session = Depends(get_db)

    @post_router.post("/posts", status_code=status.HTTP_201_CREATED)
    def create_post(self, post_data: schemas.SavePost):
        return PostCRUD.create(self.session, dict(post_data))

    @post_router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowPost])
    def get_all_posts(self):
        return PostCRUD.read_all(self.session)

    @post_router.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
    def read_post(self, post_id):
        return PostCRUD.read(self.session, post_id)

    @post_router.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
    def update_post(self, post_id, post_data: schemas.SavePost):
        return PostCRUD.update(self.session, post_id, dict(post_data))

    @post_router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_post(self, post_id):
        return PostCRUD.delete(self.session, post_id)

    @post_router.post("/posts/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
    def like_action(self, post_id, post_data: schemas.BaseLike):
        return PostCRUD.like(self.session, post_id, post_data.user_id)
