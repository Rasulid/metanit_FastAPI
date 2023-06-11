import email

from sqlalchemy import Column, Integer, String, Boolean
from .base_model import Base


class Users_Table(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    age = Column(Integer)
    password = Column(String)
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    is_verified = Column(Boolean)
