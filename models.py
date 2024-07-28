from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, mapped_column

from database import Base

class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="user")

class Book(Base):
    __tablename__ = 'books'
    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True, nullable=False)
    author = mapped_column(String, index=True, nullable=False)
    genre = mapped_column(String, index=True, nullable=False)
    year_published = mapped_column(Integer, nullable=False)
    summary = mapped_column(Text, nullable=False)


    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"
    id = mapped_column(Integer, primary_key=True, index=True)
    book_id = mapped_column(Integer, ForeignKey("books.id"))
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    review_text = mapped_column(Text, nullable=False)
    rating = mapped_column(Integer, nullable=False)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
