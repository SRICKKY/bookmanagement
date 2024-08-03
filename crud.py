from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

import llama3_service
import models
import schemas
from core.security import get_password_hash, verify_password


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)

    # Generate and save the summary
    generated_summary = llama3_service.generate_summary(book.summary)
    db_book.generated_summary = generated_summary
    await db.commit()
    await db.refresh(db_book)

    return db_book

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalars().first()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate):
    db_book = await get_book(db, book_id)
    if db_book:
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book

async def create_review(db: AsyncSession, book_id: int, review: schemas.ReviewCreate, current_user: schemas.UserRead):
    db_review = models.Review(**review.model_dump(), book_id=book_id, user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)

    # Generate and save the review summary
    generated_summary = llama3_service.generate_summary(review.review_text)
    db_review.generated_summary = generated_summary
    await db.commit()
    await db.refresh(db_review)

    return db_review

async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Review).filter(models.Review.book_id == book_id))
    return result.scalars().all()

async def get_book_summary(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        avg_rating = await db.execute(select(func.avg(models.Review.rating)).filter(models.Review.book_id == book_id))
        avg_rating = avg_rating.scalar() or 0
        return {
            "summary": db_book.summary or "No summary available.",
            "average_rating": avg_rating
        }
    return None

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def create_user(db: AsyncSession, user_data: schemas.UserCreate):
    new_user = models.User(email=user_data.email, hashed_password=get_password_hash(user_data.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user