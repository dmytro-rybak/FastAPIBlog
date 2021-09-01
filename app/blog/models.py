from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


likes_table = Table('association', Base.metadata,
                    Column('post_id', Integer, ForeignKey('post.post_id'), primary_key=True),
                    Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True))


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    posts = relationship('Post')
    liked_posts = relationship(
        "Post",
        secondary=likes_table,
        back_populates="likes")

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username


class Post(Base):
    __tablename__ = 'post'
    post_id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    likes = relationship(
        "User",
        secondary=likes_table,
        back_populates="liked_posts")

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title
