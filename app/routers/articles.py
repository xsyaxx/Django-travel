from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from slugify import slugify

from app.schemas.article import ArticleCreate, Article, ArticleUpdate
from app.models.article import Article as ArticleModel
from app.models.user import User as UserModel
from app.utils.security import get_current_user
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=Article)
async def create_article(
    article_in: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Any:
    """
    Create new article.
    """
    user = await db.query(UserModel).filter(UserModel.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_article = ArticleModel(
        title=article_in.title,
        content=article_in.content,
        slug=slugify(article_in.title),
        author_id=user.id
    )
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    return db_article

@router.get("/", response_model=List[Article])
async def read_articles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve articles.
    """
    articles = await db.query(ArticleModel).offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=Article)
async def read_article(
    article_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get article by ID.
    """
    article = await db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/{article_id}", response_model=Article)
async def update_article(
    article_id: int,
    article_in: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Any:
    """
    Update article.
    """
    user = await db.query(UserModel).filter(UserModel.email == current_user).first()
    article = await db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in article_in.dict(exclude_unset=True).items():
        if field == "title":
            setattr(article, "slug", slugify(value))
        setattr(article, field, value)
    
    await db.commit()
    await db.refresh(article)
    return article

@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Any:
    """
    Delete article.
    """
    user = await db.query(UserModel).filter(UserModel.email == current_user).first()
    article = await db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await db.delete(article)
    await db.commit()
    return {"status": "success"} 