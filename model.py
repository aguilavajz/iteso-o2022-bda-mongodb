#!/usr/bin/env python3
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Food(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    oracle_id: str = Field(...)
    filename: str = Field(...)
    name: list = Field(...)
    confidence: list = Field(...)
    porciones: float = Field(...)
    calorias: float = Field(...)
    calorias_totales: float = Field(...)
    fecha_consumo: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "oracle_id": "30",
                "filename": "accuracy",
                "name": ["Plot"],
                "confidence": [99.999999],
                "porciones": 99,
                "calorias": 99.999999,
                "calorias_totales": 99.999999,
                "fecha_consumo": "01/01/1999"
            }
        }
