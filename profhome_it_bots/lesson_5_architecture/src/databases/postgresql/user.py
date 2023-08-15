from sqlalchemy import Boolean, Column, Integer, String

from .utils import Base


class User(Base):
    """
    Model of the users table:
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
