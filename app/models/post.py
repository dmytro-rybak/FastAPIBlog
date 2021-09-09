from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

likes_table = Table('likes', Base.metadata,
                    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
                    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    likes = relationship(
        "User",
        secondary=likes_table,
        back_populates="liked_posts")

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title
