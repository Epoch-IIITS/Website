from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI(title="Epoch Learn API")


@app.get("/")
def root():
    return {"message": "Hello, Epoch Learn"}


# TODO: /health, /users/me, /users/{name}, GET and DELETE /items/{item_id}


def route_table(app):
    # TODO
    return []
