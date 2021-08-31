from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from database import get_db
from models import user_model
from schemas import user_schemas
from passlib.context import CryptContext

router = APIRouter(tags=['User'])

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@cbv(router)
class User:
    session: Session = Depends(get_db)

    @router.post("/users", status_code=status.HTTP_201_CREATED)
    def create_user(self, _user: user_schemas.User):
        hashed_pass = password_context.hash(_user.password)
        new_user = user_model.UserModel(username=_user.username, email=_user.email, password=hashed_pass)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    @router.get("/users", status_code=status.HTTP_200_OK)
    def read_all_users(self):
        users = self.session.query(user_model.UserModel).all()
        return users

    @router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
    def read_user(self, user_id):
        db_user = self.session.query(user_model.UserModel).filter(user_model.UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
        return db_user

    @router.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
    def update_user(self, user_id, _user: user_schemas.User):
        db_user = self.session.query(user_model.UserModel).filter(user_model.UserModel.id == user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
        hashed_pass = password_context.hash(_user.password)
        db_user.update({'username': _user.username, 'email': _user.email, 'password': hashed_pass})
        self.session.commit()
        return {'detail': 'done'}

    @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(self, user_id):
        db_user = self.session.query(user_model.UserModel).filter(user_model.UserModel.id == user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
        db_user.delete(synchronize_session=False)
        self.session.commit()
        return {'detail': 'Done'}
