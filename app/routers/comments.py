from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from app.schemas.comment import CommentCreate, Comment, CommentUpdate
from app.models.comment import Comment as CommentModel
from app.models.user import User as UserModel
from app.models.article import Article as ArticleModel
from app.utils.security import get_current_user
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=Comment)
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Any:
    """
    Create new comment.
    """
    user = await db.query(UserModel).filter(UserModel.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    article = await db.query(ArticleModel).filter(ArticleModel.id == comment_in.article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db_comment = CommentModel(
        content=comment_in.content,
        author_id=user.id,
        article_id=comment_in.article_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@router.get("/article/{article_id}", response_model=List[Comment])
async def read_comments(
    article_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve comments for an article.
    """
    comments = await db.query(CommentModel).filter(
        CommentModel.article_id == article_id
    ).offset(skip).limit(limit).all()
    return comments

@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Any:
    """
    Update comment.
    """
    user = await db.query(UserModel).filter(UserModel.email == current_user).first()
    comment = await db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in comment_in.dict(exclude_unset=True).items():
        setattr(comment, field, value)
    
    await db.commit()
    await db.refresh(comment)
    return comment

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
) -> Any:
    """
    Delete comment.
    """
    user = await db.query(UserModel).filter(UserModel.email == current_user).first()
    comment = await db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await db.delete(comment)
    await db.commit()
    return {"status": "success"} 