from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models, schemas, oauth2
from fastapi import Depends, HTTPException, Response, status, APIRouter
from typing import List, Optional

router = APIRouter(prefix="/vote",
                   tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def votes(vote : schemas.Vote, db: Session = Depends(get_db), 
                current_user : Session = Depends(oauth2.get_current_user)):
    
    existing_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id== vote.post_id,
                                                    models.Vote.user_id == current_user.id)
    
    if vote.dir == 1:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"User {current_user.id} already liked this post")   
        
        vote_add = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(vote_add)
        db.commit()
        db.refresh(vote_add)
        vote_count = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).count()

        return {"post liked", f"vote_count is {vote_count}"}
        
    else:
        if vote_query.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Post does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        vote_count = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).count()

        return {"post unliked", f"vote_count is {vote_count}"}

