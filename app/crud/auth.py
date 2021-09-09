from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.user import User
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from db.database import get_db

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = "08948b24bca61e48382c4cd890ff1a6506210cfc88435e050b4d47a9bfe85243"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthCRUD:
    @staticmethod
    def check_email_exists_in_db(session, email: str):
        return session.query(User).filter(User.email == email).first()

    @staticmethod
    def check_username_exists_in_db(session, username: str):
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def check_user_exists(session, email: str, username: str):
        # check user with such email
        email = AuthCRUD.check_email_exists_in_db(session, email)
        if email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with such email already exists")

        # check user with such username
        username = AuthCRUD.check_username_exists_in_db(session, username)
        if username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with such username already exists")

    @staticmethod
    def create_user(session, user_data):
        hashed_password = password_context.hash(user_data.password)
        try:
            new_user = User(username=user_data.username, email=user_data.email, password=hashed_password)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Can't create user with such parameters")
        return new_user

    @staticmethod
    def find_exists_user(session, username: str):
        user = session.query(User).filter(User.username == username).first()
        return user

    @staticmethod
    def verify_password(password, hashed_password):
        verify = password_context.verify(password, hashed_password)
        if not verify:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(session=Depends(get_db), token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = session.query(User).filter(User.username == username).first()
        return user
