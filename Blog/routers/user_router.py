from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from database import get_db
from models import user_model
from schemas import user_schemas
from crud.user_crud import UserCRUD

router = APIRouter(tags=['User'])



@cbv(router)
class User:
    session: Session = Depends(get_db)

    @router.post("/users", status_code=status.HTTP_201_CREATED)
    def create_user(self, user_data: user_schemas.User):
        return UserCRUD.create_user(self.session, user_data)

    @router.get("/users", status_code=status.HTTP_200_OK)
    def read_all_users(self):
        return UserCRUD.get_all_users(self.session)

    @router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
    def read_user(self, user_id):
        return UserCRUD.get_user(self.session, user_id)

    @router.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
    def update_user(self, user_id, user_data: user_schemas.User):
        return UserCRUD.update_user(self.session, user_id, user_data)

    @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(self, user_id):
        return UserCRUD.delete_user(self.session, user_id)
