from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
    generated_summary: Optional[str] = None

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    review_text: str
    rating: int

    model_config = ConfigDict(from_attributes=True)

class Review(ReviewBase):
    id: int
    generated_summary: Optional[str] = None

    class Config:
        from_attributes = True

class BookSummary(BaseModel):
    summary: str
    average_rating: float

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return via API
class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Properties to receive via API on login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
