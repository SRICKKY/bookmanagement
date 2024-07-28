from typing import Optional

from pydantic import BaseModel, ConfigDict


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

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    generated_summary: Optional[str] = None

    class Config:
        from_attributes = True

class BookSummary(BaseModel):
    summary: str
    average_rating: float

    model_config = ConfigDict(from_attributes=True)
