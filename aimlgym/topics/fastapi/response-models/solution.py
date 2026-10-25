r"""Reference solution for FA-12 Response Models and Status Codes.

Input and output are different models, and every endpoint declares its response model, so the
stored `password_hash` is filtered out automatically. Status codes are declared on the decorators;
conflicts and missing users raise `HTTPException`. A separate id counter guarantees ids are never
reused after deletions.
"""
import hashlib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9_]+$")
    email: str = Field(min_length=3, pattern=r"@")
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    username: str
    email: str


def create_app():
    app = FastAPI()
    users = {}
    state = {"next_id": 1}

    def find(user_id):
        if user_id not in users:
            raise HTTPException(status_code=404, detail="User not found")
        return users[user_id]

    @app.post("/users", response_model=UserOut, status_code=201)
    def create_user(user: UserIn):
        if any(u["username"] == user.username for u in users.values()):
            raise HTTPException(status_code=409, detail="Username taken")
        record = {"id": state["next_id"], "username": user.username, "email": user.email,
                  "password_hash": hashlib.sha256(user.password.encode()).hexdigest()}
        users[record["id"]] = record
        state["next_id"] += 1
        return record

    @app.get("/users", response_model=list[UserOut])
    def list_users():
        return [users[i] for i in sorted(users)]

    @app.get("/users/{user_id}", response_model=UserOut)
    def read_user(user_id: int):
        return find(user_id)

    @app.delete("/users/{user_id}", status_code=204)
    def delete_user(user_id: int):
        find(user_id)
        del users[user_id]

    return app
