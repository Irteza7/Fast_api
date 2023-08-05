from fastapi import FastAPI, HTTPException, Response, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


saved_posts = [{"title":"1st post","content":"Idk just something","rating":5,"id":1},
               {"title":"2nd post","content":"Idk just something else","rating":3,"id":2}]

post_id_counter = 3  # Variable to generate unique IDs

def find_post_index(post_id: int):
    for i, post in enumerate(saved_posts):
        if post["id"] == post_id:
            return i
    return None



@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts():
    global saved_posts
    return saved_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):

    global post_id_counter

    post_dict = post.model_dump()
    post_dict["id"] = post_id_counter
    post_id_counter+= 1
    saved_posts.append(post_dict)
    return saved_posts


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_one_post(post_id: int):
    global saved_posts

    post_index = find_post_index(post_id)

    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post id doesn't exist or already deleted")
    
    return saved_posts[post_index]

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    global saved_posts

    post_index = find_post_index(post_id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post id doesn't exist or already deleted")

    saved_posts.pop(post_index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: Post):
    global saved_posts

    post_index = find_post_index(post_id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post id doesn't exist or already deleted")
    
    post_dict = post.model_dump()
    post_dict["id"] = post_id
    saved_posts[post_index] = post_dict

    return saved_posts[post_index]