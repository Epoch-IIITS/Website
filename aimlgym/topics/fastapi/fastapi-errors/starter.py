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

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        # TODO: 404 for unknown ids
        return {"id": item_id, **stock[item_id]}

    # TODO: POST /items/{item_id}/buy and the two exception handlers
    return app
