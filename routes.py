#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Book, BookUpdate

router = APIRouter()

@router.post("/", response_description="Post a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_book

@router.get("/", response_description="Get all books", response_model=List[Book])
def list_books(request: Request, title:str = "", avg_rating: float = 0, pages:int = 0, limit: int = 5, offset: int = 0):
    #books = list(request.app.database["books"].find(limit=100))
    #return books
    if title != "":
        books = list(request.app.database["books"].find({"$text": {"$search": title}, "average_rating": {"$gte":avg_rating},"num_pages": {"$gte":pages}}).skip(offset).limit(limit))
    else:
        books = list(request.app.database["books"].find({"average_rating": {"$gte":avg_rating},"num_pages": {"$gte":pages}}).skip(offset).limit(limit))

    return books

@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book (ID={id}) does not exists")

@router.put("/{id}", response_description="Post a new bok", status_code=status.HTTP_200_OK, response_model=Book)
def update_book(id: str, request: Request, json = Body(...) ):
    
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        json = jsonable_encoder(json)
        filter = { "_id": id }
        new = {"$set" : json}
        request.app.database["books"].update_one(filter, new)
        book = request.app.database["books"].find_one({"_id": id})
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book (ID={id}) does not exists")

@router.delete("/{id}", response_description="Delete a book", status_code=status.HTTP_200_OK)
def delete_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        request.app.database["books"].delete_one({"_id": id})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book (ID={id}) does not exists")