from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Column, Integer, String
from models.post import likes_table


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String)
    posts = relationship('Post')
    liked_posts = relationship("Post", secondary=likes_table, back_populates="likes")

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username
