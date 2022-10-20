#!/usr/bin/env python3
import argparse
import json
import logging
import os
import requests
import urllib

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('books.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv("BOOKS_API_URL", "http://localhost:8000")



def print_book(book):
    for k in book.keys():
        print(f"{k}: {book[k]}")
    print("="*50)
def list_books(request: Request, title:str = "", avg_rating: float = 0, limit: int = 5, offset: int = 0, pages:int = 0):
#def list_books(rating):
    suffix = "/book"
    endpoint = BOOKS_API_URL + suffix
    params = {
        "rating": rating
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for book in json_resp:
            print_book(book)
    else:
        print(f"Error: {response}")


def get_book_by_id(id):
    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_book(json_resp)
    else:
        print(f"Error: {response}")


def update_book(id):
    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    book = {
        "publisher": "V2ntage"
    }
    response = requests.put(endpoint, json=book)
    if response.ok:
        print("Book updated")
    else:
        print(f"Error: {response}")

def delete_book(id):
    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    response = requests.delete(endpoint)
    if response.ok:
        print("Book deleted")
    else:
        print(f"Error: {response}")

def main():
    log.info(f"Welcome to books catalog. App requests to: {BOOKS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    parser.add_argument("-i", "--id",
            help="Provide a book ID which related to the book action", default=None)
    parser.add_argument("-r", "--rating",
            help="Search parameter to look for books with average rating equal or above the param (0 to 5)", default=None)

    args = parser.parse_args()

    if args.id and not args.action in ["get", "update", "delete"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if args.rating and args.action != "search":
        log.error(f"Rating arg can only be used with search action")
        exit(1)

    if args.action == "search":
        list_books(args.rating)
    elif args.action == "get" and args.id:
        get_book_by_id(args.id)
    elif args.action == "update":
        update_book(args.id)
    elif args.action == "delete":
        delete_book(args.id)

if __name__ == "__main__":
    main()