from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from .dababase import Base 

# Custom UUID Type for SQLite
class GUID(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        try:
            return uuid.UUID(value)  
        except ValueError:
            return None 

class Role(PyEnum):
    Admin = "Admin"
    User = "User"
    SuperAdmin = "SuperAdmin"

class User(Base):
    __tablename__ = 'users'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    FullName = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)
    Role = Column(Enum(Role), default=Role.User)
    CreatedAt = Column(DateTime, default=datetime.now(timezone.utc))
    UpdatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    DeletedAt = Column(DateTime, nullable=True)
    Active = Column(Boolean, default=True)
    refreshToken = Column(String, unique=True, nullable=True)
    
    snippets = relationship("Snippet_code", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Snippet_code(Base):
    __tablename__ = 'snippet_codes'
    ID = Column(GUID(), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)
    Code = Column(String, nullable=False)
    Language = Column(String, nullable=False)
    Description = Column(String, nullable=True)
    UserId = Column(GUID(), ForeignKey('users.id'))
    CategoryId = Column(GUID(), ForeignKey('categories.id'))
    
    CreatedAt = Column(DateTime, default=datetime.now(timezone.utc))
    UpdatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    category = relationship("Category", back_populates="snippets")
    user = relationship("User", back_populates="snippets")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    Name = Column(String, nullable=False)
    UserId = Column(GUID(), ForeignKey('users.id'))
    CreatedAt = Column(DateTime, default=datetime.now(timezone.utc))
    UpdatedAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="categories")
    snippets = relationship("Snippet_code", back_populates="category")
