from sqlalchemy import Column, Integer, String, DateTime, func
from src.app.database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")


# Pydantic 스키마
class PostCreate(BaseModel):
    author: str
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    author: str
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
