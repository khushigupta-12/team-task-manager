from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:ebHzhPuDYgwXjMSyvEhkGtxLYpGzRcdx@switchyard.proxy.rlwy.net:15084/railway"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()