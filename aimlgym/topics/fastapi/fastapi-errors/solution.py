r"""Reference solution for FA-11 Handling Errors in FastAPI.

A shared `find` helper raises the 404 in one place. The purchase logic raises a domain exception
that knows nothing about HTTP, and the handler maps it to 409 with a structured body. Overriding
the validation handler changes every 422 in the app. Because the stock dict lives inside the
factory, each `create_app()` call starts from the same state.
"""
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class OutOfStock(Exception):
    def __init__(self, item, requested, available):
        super().__init__(f"{item}: requested {requested}, available {available}")
        self.item, self.requested, self.available = item, requested, available


def create_app():
    app = FastAPI()
    stock = {1: {"name": "pen", "stock": 3}, 2: {"name": "ink", "stock": 0}}

    def find(item_id):
        if item_id not in stock:
            raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "missing"})
        return stock[item_id]

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"id": item_id, **find(item_id)}

    @app.post("/items/{item_id}/buy")
    def buy(item_id: int, qty: Annotated[int, Query(ge=1)] = 1):
        entry = find(item_id)
        if qty > entry["stock"]:
            raise OutOfStock(entry["name"], qty, entry["stock"])
        entry["stock"] -= qty
        return {"item": entry["name"], "remaining": entry["stock"]}

    @app.exception_handler(OutOfStock)
    async def out_of_stock(request: Request, exc: OutOfStock):
        return JSONResponse(status_code=409, content={"error": "out_of_stock", "item": exc.item,
                                                      "requested": exc.requested, "available": exc.available})

    @app.exception_handler(RequestValidationError)
    async def validation(request: Request, exc: RequestValidationError):
        fields = [".".join(str(p) for p in e["loc"]) for e in exc.errors()]
        return JSONResponse(status_code=422, content={"error": "validation_error", "fields": fields})

    return app
