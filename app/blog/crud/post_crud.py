from fastapi import status, HTTPException
from blog import models


class PostCRUD:

    @staticmethod
    def create(session, post_data):
        try:
            new_post = models.Post(**post_data)
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Cant create post with such parameters")
        return new_post

    @staticmethod
    def read(session, post_id):
        post = session.query(models.Post).filter(models.Post.post_id == post_id).first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {post_id} is not found")

        return post

    @staticmethod
    def read_all(session):
        posts = session.query(models.Post).read_all()
        return posts

    @staticmethod
    def update(session, post_id, post_data):
        post = session.query(models.Post).filter(models.Post.post_id == post_id).first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {post_id} is not found")

        try:
            post.update(**post_data)
            session.commit()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Cant create post with such parameters")

        return post

    @staticmethod
    def delete(session, post_id):
        post = session.query(models.Post).filter(models.Post.post_id == post_id)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {post_id} is not found")

        post.delete(synchronize_session=False)
        session.commit()

        return {'detail': 'Post deleted'}

    @staticmethod
    def like(session, post_id, user_id):
        post = session.query(models.Post).filter(models.Post.post_id == post_id).first()
        user = session.query(models.User).filter(models.User.user_id == user_id).first()

        if not post and not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {post_id} is not found")

        if user in post.likes:
            post.likes.remove(user)
        else:
            post.likes.append(user)

        session.commit()

        return {'detail': 'Test'}
