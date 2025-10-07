from sqlalchemy.orm import Session
from src.app.models.post import PostCreate
from src.app.models import Post
from fastapi import Depends
from src.app.database import get_db
from sqlalchemy import select

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post_data: PostCreate) -> Post:
        new_post = Post(**post_data.model_dump())
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)
        return new_post
    def get_post(self):
        query = (
            select(Post).order_by(Post.created_at.desc())
        )
        posts = self.db.execute(query).scalars().all()
        return posts

    def get_post_by_id(self, post_id: int):
        query = select(Post).where(Post.id == post_id)
        post_item = self.db.execute(query).scalar_one_or_none()
        return post_item

    def update_post(self, post_id: int, post_data: PostCreate):
        query = select(Post).where(Post.id == post_id)
        post_item = self.db.execute(query).scalar_one_or_none()
        if post_item is None:
            return None

        for key, value in post_data.model_dump().items():
            setattr(post_item, key, value)

        self.db.commit()
        self.db.refresh(post_item)
        return post_item

    def delete_post(self, post_id: int):
        query = (
            select(Post).
            where(Post.id == post_id)
        )
        post_item = self.db.execute(query).scalar_one_or_none()
        if post_item is None:
            return None

        self.db.delete(post_item)
        self.db.commit()
        return True

def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)
