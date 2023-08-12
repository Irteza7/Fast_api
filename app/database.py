from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgres://{settings.database_username}:\
    {settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# SQLALCHEMY_DATABASE_URL = {settings.db_url}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try: 
#         conn = psycopg2.connect(host = "****", database = "****", 
#                                 user = "****", password = "****", 
#                                 cursor_factory = RealDictCursor)
#         cursor= conn.cursor()
#         print("Connection successfull!")
#         break
#     except Exception as e:
#         print("Connection could not be made: {e}")
#         time.sleep(3)