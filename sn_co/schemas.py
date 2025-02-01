from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    User = "User"
    Admin = "Admin"
    SuperAdmin = "SuperAdmin"

class UserBase(BaseModel):
    FullName: str
    Email: str
    Role: Role
    CreatedAt: datetime
    UpdatedAt: datetime
    DeletedAt: Optional[datetime] = None
    Active: bool
    refreshToken: Optional[str] = None

    class Config:
        from_attributes = True  

class UserCreate(UserBase):
    Password: str

class SnippetBase(BaseModel):
    title: str
    Code: str
    Language: str
    Description: Optional[str] = None
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True  

class CategoryBase(BaseModel):
    Name: str
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True  
