from fastapi import Depends, APIRouter, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import login
from crud.auth import AuthCRUD
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@cbv(router)
class Auth:
    session: Session = Depends(get_db)

    @router.post("/register", status_code=status.HTTP_201_CREATED)
    def register_new_user(self, user_data: login.UserValidate):
        AuthCRUD.check_user_exists(self.session, email=user_data.email, username=user_data.username)
        return AuthCRUD.create_user(self.session, user_data)

    @router.post('/login', status_code=status.HTTP_200_OK)
    def access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        db_user = AuthCRUD.find_exists_user(self.session, form_data.username)
        AuthCRUD.verify_password(password=form_data.password, hashed_password=db_user.password)
        access_token = AuthCRUD.create_access_token(data={'sub': form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
