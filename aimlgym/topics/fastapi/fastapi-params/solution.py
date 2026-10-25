r"""Reference solution for FA-09 Query and Path Parameters with Validation.

All validation is declared in the signatures, so the bodies only filter, sort and slice. The Enum
restricts `order` to two strings, `Path` bounds the year, and the list-typed query parameter
collects repeated `tag` values. FastAPI produces 422 responses for every rule violation before the
function runs.
"""
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


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


@app.get("/books")
def list_books(
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=5)] = 3,
    offset: Annotated[int, Query(ge=0)] = 0,
    order: Order = Order.asc,
):
    matches = [b for b in BOOKS if q is None or q.lower() in b["title"].lower()]
    matches = sorted(matches, key=lambda b: (b["year"], b["id"]), reverse=order == Order.desc)
    return {"count": len(matches), "items": matches[offset:offset + limit]}


@app.get("/books/by-year/{year}")
def books_by_year(year: Annotated[int, Path(ge=1900, le=2100)]):
    return [b["title"] for b in BOOKS if b["year"] == year]


@app.get("/books/tagged")
def books_tagged(tag: Annotated[list[str], Query()] = []):
    wanted = set(tag)
    return [b["id"] for b in BOOKS if wanted <= set(b["tags"])]
