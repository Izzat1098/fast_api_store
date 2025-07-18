from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    user_name = Column(String, unique=True, index=True, nullable=False)  
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)