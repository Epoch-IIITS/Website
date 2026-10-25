r"""Reference solution for FA-08 First FastAPI Routes.

Each decorator registers one path operation; type hints drive conversion and validation, so the
handlers contain only the response logic. Declaring the fixed `/users/me` route first keeps it
from being captured by the parameterised route. `route_table` reads the same registry FastAPI
uses for routing and for the OpenAPI schema.
"""
from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI(title="Epoch Learn API")


@app.get("/")
def root():
    return {"message": "Hello, Epoch Learn"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users/me")
def read_me():
    return {"user": "current"}


@app.get("/users/{name}")
def read_user(name: str):
    return {"user": name}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "double": 2 * item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted": item_id}


def route_table(app):
    return sorted((m, r.path) for r in app.routes if isinstance(r, APIRoute) for m in r.methods)
