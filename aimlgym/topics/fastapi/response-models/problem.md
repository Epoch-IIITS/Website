# FA-12 · Response Models and Status Codes

**Topic:** FastAPI · **Difficulty:** advanced · **Allowed packages:** fastapi

**Builds on:** FA-11 Handling Errors in FastAPI

Read the lesson first: [article.md](article.md)

## Task

Define `UserIn` and `UserOut` as in the lesson and `create_app()` with an in-memory store (ids
start at 1 and are never reused):

* `POST /users` → 201 `UserOut`; store `{"id", "username", "email", "password_hash"}` with
  `hashlib.sha256(password.encode()).hexdigest()`; an existing username → 409 `{"detail":
  "Username taken"}`.
* `GET /users` → list of `UserOut` in id order.
* `GET /users/{user_id}` → `UserOut` or 404 `{"detail": "User not found"}`.
* `DELETE /users/{user_id}` → 204 with an empty body, or 404.

Endpoints should return the stored dicts; the response model must remove `password_hash`.

## Hints

<details><summary>Hint 1</summary>

Add `response_model=UserOut, status_code=201` to the POST decorator and store `password_hash` instead of `password`.

</details>

<details><summary>Hint 2</summary>

Keep a counter (e.g. `state = {"next_id": 1}`) so deleted ids are not reused; check for an existing username first.

</details>

<details><summary>Hint 3</summary>

`@app.delete("/users/{user_id}", status_code=204)` and return `None`; `response_model=list[UserOut]` for the list.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_create_201_without_secrets` | Use `response_model=UserOut` and `status_code=201`, and never store the raw password. |
| `test_input_validation` | Add the username pattern and length limits, the email pattern and an 8-character password minimum. |
| `test_duplicate_409` | Check for an existing username before creating and raise HTTPException(409). |
| `test_list_and_read` | Use `response_model=list[UserOut]` for the list and return 404 for unknown ids. |
| `test_delete_204_and_no_reuse` | Declare `status_code=204`, return None, and keep a separate id counter. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Input and output are different models, and every endpoint declares its response model, so the
stored `password_hash` is filtered out automatically. Status codes are declared on the decorators;
conflicts and missing users raise `HTTPException`. A separate id counter guarantees ids are never
reused after deletions.

## References

- [FastAPI Tutorial: Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/) — FastAPI (Sebastián Ramírez) (`S075`)
- [FastAPI Tutorial: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — FastAPI (Sebastián Ramírez) (`S070`)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — MDN Web Docs (Mozilla) (`S066`)
