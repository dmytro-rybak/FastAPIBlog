from fastapi import Depends, APIRouter, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from db.database import get_db
from blog import schemas
from blog.crud.user_crud import UserCRUD
from typing import List

user_router = APIRouter(tags=['User'])


@cbv(user_router)
class User:
    session: Session = Depends(get_db)

    @user_router.post("/users", status_code=status.HTTP_201_CREATED)
    def create_user(self, user_data: schemas.BaseUser):
        return UserCRUD.create_user(self.session, user_data)

    @user_router.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
    def read_all_users(self):
        return UserCRUD.get_all_users(self.session)

    @user_router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
    def read_user(self, user_id):
        return UserCRUD.get_user(self.session, user_id)

    @user_router.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
    def update_user(self, user_id, user_data: schemas.BaseUser):
        return UserCRUD.update_user(self.session, user_id, user_data)

    @user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(self, user_id):
        return UserCRUD.delete_user(self.session, user_id)
