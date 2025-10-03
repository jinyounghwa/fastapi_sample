from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    author: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    created_at: str

    class Config:
        orm_mode = True