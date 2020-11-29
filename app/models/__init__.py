from pydantic import BaseModel, EmailStr
import enum

from typing import Optional


class Role(enum.Enum):
    admin = 'admin'
    visitor = 'visitor'


class User(BaseModel):
    email: EmailStr
    password: str
    role: Optional[Role]


class Author(BaseModel):
    name: str


class Book(BaseModel):
    isbn: str
    name: str
    year: int


