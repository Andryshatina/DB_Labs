import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/lab1'
Orders = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)