import os
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    short = Column(String, primary_key=True, index=True)
    original = Column(String, unique=True, index=True)

def init_db():
    Base.metadata.create_all(bind=engine)
