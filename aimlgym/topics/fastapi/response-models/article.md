# Response Models and Status Codes

## Learning outcomes

After this lesson you can:

- Separate input and output models so secrets never leave the API
- Set success status codes such as 201 and 204
- Return lists of models and handle conflicts with 409
- Store a password hash instead of the password

## Intuition
What a client sends and what it should get back are different. A sign-up request contains a
password; the response must never include it. FastAPI's **response model** filters every response
through a Pydantic class, so a field that is not in the output model cannot leak, even if your
function returns it by mistake.

## Precise explanation
```python
class UserIn(BaseModel):            # what clients send
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9_]+$")
    email: str = Field(min_length=3, pattern=r"@")
    password: str = Field(min_length=8)

class UserOut(BaseModel):           # what clients receive
    id: int
    username: str
    email: str

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn): ...   # may return a dict with extra keys: they are dropped

@app.get("/users", response_model=list[UserOut])
@app.delete("/users/{user_id}", status_code=204)   # return None → empty body
```
* **201 Created** for successful creation, **204 No Content** for deletion, **409 Conflict** for
  duplicates, **404** for missing resources.
* `pattern=` validates strings with a regular expression (NL-01).
* **Passwords**: store only a hash. This lesson uses `hashlib.sha256` to show the idea; real
  systems must use a slow, salted password hash such as Argon2 or bcrypt.
* CRUD = Create, Read, Update, Delete — the basic operations of a resource API.

## Worked example
`POST /users {"username": "ada", "email": "ada@x.org", "password": "correct horse"}` → 201
`{"id": 1, "username": "ada", "email": "ada@x.org"}` — no `password`, no hash.

## Common mistakes
* Returning the stored record (with its hash) without a response model.
* Using 200 for creation and deletion, so clients cannot tell what happened.
* Returning a body with 204.

## Why this matters
Response models are both a security boundary and documentation: the OpenAPI schema shows exactly
what each endpoint returns.

## References

- [FastAPI Tutorial: Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/) — FastAPI (Sebastián Ramírez) (`S075`)
- [FastAPI Tutorial: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — FastAPI (Sebastián Ramírez) (`S070`)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — MDN Web Docs (Mozilla) (`S066`)
