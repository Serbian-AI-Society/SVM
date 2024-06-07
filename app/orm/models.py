from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    email = Column(String, unique=True, index=True)
