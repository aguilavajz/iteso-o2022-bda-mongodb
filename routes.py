#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Book, BookUpdate, Food

router = APIRouter()

@router.post("/", response_description="Save to Mongo", status_code=status.HTTP_201_CREATED, response_model=Food)
def create_book(request: Request, food: Food = Body(...)):
    food = jsonable_encoder(food)
    new_food = request.app.database["books"].insert_one(food)
    #created_book = request.app.database["books"].find_one(
    #    {"_id": new_book.inserted_id}
    #)
    return food

@router.get("/", response_description="Get all foods", response_model=List[Food])
def list_books(request: Request, filename:str = "", confidence: float = 0, name:str = "", pages:int = 0, limit: int = 5, offset: int = 0):
    #books = list(request.app.database["books"].find(limit=100))
    #return books
    if title != "":
        books = list(request.app.database["books"].find({"$text": {"$search": filename}, "confidence": {"$gte":confidence}}).skip(offset).limit(limit))
    else:
        books = list(request.app.database["books"].find({"confidence": {"$gte":confidence}}).skip(offset).limit(limit))

    return books

@router.get("/{id}", response_description="Get a single record", response_model=Food)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"oracle_id": id})) is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book (ID={id}) does not exists")

@router.put("/{id}", response_description="Update food", status_code=status.HTTP_200_OK, response_model=Food)
def update_book(id: str, request: Request, json = Body(...) ):
    
    if (book := request.app.database["books"].find_one({"oracle_id": id})) is not None:
        json = jsonable_encoder(json)
        filter = { "oracle_id": id }
        new = {"$set" : json}
        request.app.database["books"].update_one(filter, new)
        book = request.app.database["books"].find_one({"oracle_id": id})
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food (ID={id}) does not exists")

@router.delete("/{id}", response_description="Delete a food", status_code=status.HTTP_200_OK)
def delete_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"oracle_id": id})) is not None:
        request.app.database["books"].delete_one({"oracle_id": id})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food (ID={id}) does not exists")