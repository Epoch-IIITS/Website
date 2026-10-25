# Dependencies and Dependency Overrides

## Learning outcomes

After this lesson you can:

- Share setup code between endpoints with Depends
- Authenticate with an API-key header dependency that raises 401
- Write dependencies with cleanup using yield
- Replace dependencies in tests with app.dependency_overrides

## Intuition
Many endpoints need the same things: a database connection, the current user, paging options.
Instead of repeating that code, an endpoint *declares* what it needs with `Depends(...)`, and
FastAPI calls the provider function for each request. In tests you can swap any provider for a
fake — without touching the endpoints.

## Precise explanation
```python
def get_store():                     # a dependency is just a function
    return STORE

def current_user(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key not in API_KEYS:    # header X-API-Key (underscores become dashes)
        raise HTTPException(401, "Invalid API key", headers={"WWW-Authenticate": "ApiKey"})
    return API_KEYS[x_api_key]

@app.get("/notes")
def list_notes(user: Annotated[str, Depends(current_user)],
               store: Annotated[NoteStore, Depends(get_store)]): ...
```
* Dependencies can have their own parameters (query, headers, other dependencies); FastAPI
  validates them like endpoint parameters and documents them.
* **yield dependencies** run setup, hand over a value, and run cleanup after the response:
  ```python
  def request_log():
      EVENTS.append("open")
      try:
          yield EVENTS          # the endpoint runs here
      finally:
          EVENTS.append("close")
  ```
  A function containing `yield` pauses at that line; FastAPI resumes it after the endpoint. Use it
  for database sessions, files or locks.
* **Overrides**: `app.dependency_overrides[get_store] = lambda: fake_store` makes every endpoint
  that depends on `get_store` receive the fake. This is how tests avoid real databases and real
  credentials (PY-27's fakes, applied to an API).
* Security note: compare secrets with `hmac.compare_digest` in real systems; a dict lookup is
  used here for clarity.

## Worked example
Without the header, `GET /notes` → 401. With `X-API-Key: key-ada`, the endpoint receives
`user="ada"` and the store, and returns Ada's notes.

## Common mistakes
* Calling the dependency yourself (`Depends(get_store())`) instead of passing the function.
* Module-level state shared between tests — override the store with a fresh one per test.
* Forgetting to clear `dependency_overrides` when reusing one app across tests.

## Why this matters
Dependencies keep endpoints small and testable; FA-14 uses an overridable dependency
to replace a slow external service with a fake.

## References

- [FastAPI Tutorial: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) — FastAPI (Sebastián Ramírez) (`S076`)
- [FastAPI Advanced: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) — FastAPI (Sebastián Ramírez) (`S079`)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html) — Python Software Foundation (`S064`)
