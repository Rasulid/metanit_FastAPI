# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
#
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///identifier.sqlite"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# # engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
#
# Base = declarative_base()
#
# Base = declarative_base()
#
#
# class Person(Base):
#     __tablename__ = "people"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     age = Column(Integer)
#
#
#
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )


SessionLocal = sessionmaker(autoflush=False, bind=engine)