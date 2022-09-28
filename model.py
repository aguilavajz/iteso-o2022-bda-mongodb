#!/usr/bin/env python3
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    authors: list = Field(...)
    average_rating: float = Field(...)
    isbn: str = Field(...)
    isbn13: str = Field(...)
    language_code: str = Field(...)
    num_pages: int = Field(...)
    ratings_count: int = Field(...)
    text_reviews_count: int = Field(...)
    publication_date: str = Field(...)
    publisher: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Poor People",
                "authors": ["William T. Vollmann"],
                "average_rating": 3.5,
                "isbn": "0060878827",
                "isbn13": "9780060878825",
                "language_code": "eng",
                "num_pages": 434,
                "ratings_count": 769,
                "text_reviews_count": 139,
                "publication_date": "2/27/2007",
                "publisher": "Ecco"
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    authors: Optional[list]
    average_rating: Optional[float]
    isbn: Optional[str]
    isbn13: Optional[str]
    language_code: Optional[str]
    num_pages: Optional[int]
    ratings_count: Optional[int]
    text_reviews_count: Optional[int]
    publication_date: Optional[str]
    publisher:  Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Poor People",
                "authors": ["William T. Vollmann"],
                "average_rating": 3.5,
                "isbn": "0060878827",
                "isbn13": "9780060878825",
                "language_code": "eng",
                "num_pages": 434,
                "ratings_count": 769,
                "text_reviews_count": 139,
                "publication_date": "2/27/2007",
                "publisher": "Ecco"
            }
        }