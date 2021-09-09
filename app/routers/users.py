from fastapi import Depends, APIRouter, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud.auth import AuthCRUD
from db.database import get_db
from schemas import user, login
from crud.base_crud import BaseCRUD
from typing import List
from models.user import User

router = APIRouter()


@cbv(router)
class User:
    db: Session = Depends(get_db)
    user_crud = BaseCRUD(User)

    @router.get('/me', status_code=status.HTTP_200_OK, response_model=user.ShowUser)
    def read_current_user(self, cur_user=Depends(AuthCRUD.get_current_user)):
        return self.user_crud.read(db=self.db, obj_id=cur_user.id)

    @router.get("/", status_code=status.HTTP_200_OK, response_model=List[user.ShowUser])
    def read_all_users(self):
        return self.user_crud.read_all(db=self.db)

    @router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=user.ShowUser)
    def read_user(self, user_id):
        return self.user_crud.read(db=self.db, obj_id=user_id)

    @router.put("/me", status_code=status.HTTP_202_ACCEPTED, response_model=login.UserShow)
    def update_current_user(self, user_data: login.UserShow, cur_user=Depends(AuthCRUD.get_current_user)):
        return self.user_crud.update(db=self.db, obj_id=cur_user.id, new_obj_data=dict(user_data))

    @router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
    def delete_current_user(self, cur_user=Depends(AuthCRUD.get_current_user)):
        return self.user_crud.delete(db=self.db, obj_id=cur_user.id)
