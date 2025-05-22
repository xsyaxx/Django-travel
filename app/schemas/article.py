from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    content: str
    slug: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleInDBBase(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class Article(ArticleInDBBase):
    pass 