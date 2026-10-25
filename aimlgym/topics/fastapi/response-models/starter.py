import hashlib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


def create_app():
    app = FastAPI()
    users = {}

    @app.post("/users")
    def create_user(user: UserIn):
        record = {"id": len(users) + 1, **user.model_dump()}
        users[record["id"]] = record
        return record

    # TODO: constraints, status codes, response models, hashing, the other endpoints
    return app
