from fastapi import FastAPI
from app.database import engine
from app.routers import post, user, auth
from app.config import settings
from app import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)