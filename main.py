#!/usr/bin/env python3
import os

from fastapi import FastAPI
from pymongo import MongoClient
from routes import router as book_router


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://aguilavajz:T4t13584@aguilavajz.bsrrgui.mongodb.net/?retryWrites=true&w=majority')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'iteso')

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")

app.include_router(book_router, tags=["books"], prefix="/book")