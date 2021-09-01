from fastapi import status, HTTPException
from blog import models
from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserCRUD:
    @staticmethod
    def create_user(session, user_data):
        hashed_password = password_context.hash(user_data.password)
        try:
            new_user = models.User(username=user_data.username, email=user_data.email, password=hashed_password)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cant create user with such parameters")

        return new_user

    @staticmethod
    def get_user(session, user_id):
        db_user = session.query(models.User).filter(models.User.user_id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
        return db_user

    @staticmethod
    def get_all_users(session):
        users = session.query(models.User).read_all()
        return users

    @staticmethod
    def update_user(session, user_id, user_data):
        db_user = session.query(models.User).filter(models.User.user_id == user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")

        hashed_pass = password_context.hash(user_data.password)
        try:
            db_user.update({'username': user_data.username, 'email': user_data.email, 'password': hashed_pass})
            session.commit()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cant create user with such parameters")

        return {'detail': 'done'}

    @staticmethod
    def delete_user(session, user_id):
        db_user = session.query(models.User).filter(models.User.user_id == user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
        db_user.delete(synchronize_session=False)
        session.commit()
        return {'detail': 'User deleted'}
