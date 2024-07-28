from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from core.security import get_current_user
from database import get_session_local

books_router = router = APIRouter()

@router.post("/", response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate, 
    db: AsyncSession = Depends(get_session_local), 
    current_user: schemas.UserRead = Depends(get_current_user)):
    return await crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
async def get_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session_local)):
    books = await crud.get_books(db=db, skip=skip, limit=limit)
    return books

@router.get("/{id}", response_model=schemas.Book)
async def get_book(id: int, db: AsyncSession = Depends(get_session_local)):
    book = await crud.get_book(db=db, book_id=id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{id}", response_model=schemas.Book)
async def update_book(
    id: int, 
    book: schemas.BookUpdate, 
    db: AsyncSession = Depends(get_session_local), 
    current_user: schemas.UserRead = Depends(get_current_user)):
    updated_book = await crud.update_book(db=db, book_id=id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{id}", response_model=schemas.Book)
async def delete_book(
    id, 
    db: AsyncSession = Depends(get_session_local), 
    current_user: schemas.UserRead = Depends(get_current_user)):
    deleted_book = await crud.delete_book(db=db, book_id=id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book

@router.post("/{id}/reviews", response_model=schemas.Review)
async def create_review(
    id: int, 
    review: schemas.ReviewCreate, 
    db: AsyncSession = Depends(get_session_local), 
    current_user: schemas.UserRead = Depends(get_current_user)):
    return await crud.create_review(db=db, book_id=id, review=review, current_user=current_user)

@router.get("/{id}/reviews", response_model=List[schemas.Review])
async def get_reviews(id: int, db: AsyncSession = Depends(get_session_local)):
    reviews = await crud.get_reviews(db=db, book_id=id)
    return reviews

@router.get("/{id}/summary", response_model=schemas.BookSummary)
async def get_book_summary(id: int, db: AsyncSession = Depends(get_session_local)):
    summary = await crud.get_book_summary(db=db, book_id=id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return summary
