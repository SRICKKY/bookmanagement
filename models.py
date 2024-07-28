from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    author = mapped_column(String)
    genre = mapped_column(String)
    year_published = mapped_column(Integer)
    summary = mapped_column(Text)

    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"

    id = mapped_column(Integer, primary_key=True, index=True)
    book_id = mapped_column(Integer, ForeignKey("books.id"))
    user_id = mapped_column(Integer)
    review_text = mapped_column(Text)
    rating = mapped_column(Integer)

    book = relationship("Book", back_populates="reviews")
