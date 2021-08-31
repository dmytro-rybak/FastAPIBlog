from database import Base
from sqlalchemy import Column, Integer, String, Float


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __str__(self):
        return self.username
