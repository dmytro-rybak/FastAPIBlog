from fastapi import Depends, APIRouter, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import post
from crud.post import PostCRUD
from typing import List

router = APIRouter()


@cbv(router)
class Post:
    session: Session = Depends(get_db)

    @router.post("/", status_code=status.HTTP_201_CREATED)
    def create_post(self, post_data: post.SavePost):
        return PostCRUD.create(self.session, dict(post_data))

    @router.get("/", status_code=status.HTTP_200_OK, response_model=List[post.ShowPost])
    def get_all_posts(self):
        return PostCRUD.read_all(self.session)

    @router.get("/{post_id}", status_code=status.HTTP_200_OK)
    def read_post(self, post_id):
        return PostCRUD.read(self.session, post_id)

    @router.put("/{post_id}", status_code=status.HTTP_202_ACCEPTED)
    def update_post(self, post_id, post_data: post.SavePost):
        return PostCRUD.update(self.session, post_id, dict(post_data))

    @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_post(self, post_id):
        return PostCRUD.delete(self.session, post_id)

    @router.post("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
    def like_action(self, post_id, post_data: post.BaseLike):
        return PostCRUD.like(self.session, post_id, post_data.user_id)
