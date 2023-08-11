from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models, schemas, oauth2
from fastapi import Depends, HTTPException, Response, status, APIRouter
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])



# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
@router.get("/" , response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user), 
                    limit: int=10, skip: int = 0, search: Optional[str]= ""):
    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts_with_vote_counts = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = list(map(lambda x:x._mapping,posts_with_vote_counts))

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING * """,
    #                  (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title,content=post.content,published=post.published)

    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
async def get_one_post(post_id: int, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (post_id,))
    # fetched_post = cursor.fetchone()

    # fetched_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    fetched_post = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).\
                    join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
                    group_by(models.Post.id).filter(models.Post.id == post_id).first()

    if fetched_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {post_id} does not exist")
    
    return fetched_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
    # deleted_post = cursor.fetchone()

    
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Post id {post_id} doesn't exist or already deleted")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail= "User is not authorized to delete this post")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == post_id)
    
    if query_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id {post_id} doesn't exist")

    query_post.update(post.model_dump())

    return query_post.first()