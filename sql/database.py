from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABSE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABSE_URL, connect_args={"check_same_thread": False}
)
# each session instance is a database session, but this is just a class creator
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# declaritive base also returns a class
Base = declarative_base()
# we will later inherit form Base to make our ORM classes/models


