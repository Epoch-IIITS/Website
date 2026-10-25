from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query

BOOKS = [
    {"id": 1, "title": "Deep Learning", "year": 2016, "tags": ["dl", "ml"]},
    {"id": 2, "title": "Pattern Recognition and Machine Learning", "year": 2006, "tags": ["ml", "stats"]},
    {"id": 3, "title": "Reinforcement Learning", "year": 2018, "tags": ["rl", "ml"]},
    {"id": 4, "title": "Speech and Language Processing", "year": 2024, "tags": ["nlp"]},
    {"id": 5, "title": "Dive into Deep Learning", "year": 2023, "tags": ["dl", "ml"]},
    {"id": 6, "title": "Think Stats", "year": 2014, "tags": ["stats"]},
]

app = FastAPI()


@app.get("/books")
def list_books(q: str | None = None, limit: int = 3, offset: int = 0):
    # TODO: validation, Enum order, filtering, sorting, paging
    return {"count": len(BOOKS), "items": BOOKS[:limit]}


# TODO: /books/by-year/{year} and /books/tagged
