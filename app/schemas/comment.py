from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    article_id: int

class CommentUpdate(CommentBase):
    pass

class CommentInDBBase(CommentBase):
    id: int
    author_id: int
    article_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class Comment(CommentInDBBase):
    pass 