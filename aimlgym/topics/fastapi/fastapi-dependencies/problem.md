# FA-13 · Dependencies and Dependency Overrides

**Topic:** FastAPI · **Difficulty:** advanced · **Allowed packages:** fastapi

**Builds on:** FA-12 Response Models and Status Codes

Read the lesson first: [article.md](article.md)

## Task

Implement:

* `class NoteStore` with `add(owner, text)` → note dict `{"id", "owner", "text"}` (ids from 1)
  and `for_owner(owner)` → that owner's notes in id order.
* `STORE = NoteStore()`; `get_store()` returns it.
* `API_KEYS = {"key-ada": "ada", "key-bob": "bob"}`; `current_user` reads header `X-API-Key` and
  raises 401 (`detail="Invalid API key"`, header `WWW-Authenticate: ApiKey`) when missing/unknown.
* `pagination(limit: 1–50 default 10, offset: ≥ 0 default 0)` → `{"limit", "offset"}`.
* `EVENTS = []` and the `request_log` yield dependency from the lesson.
* `create_app()` with:
  * `POST /notes` (body `{"text": ...}` with a non-empty string, model `NoteIn`) → 201 note,
    owned by the current user;
  * `GET /notes` → the current user's notes, paged by `pagination`; this endpoint also depends
    on `request_log` (append `"list"` to the log inside the endpoint).

## Hints

<details><summary>Hint 1</summary>

`note = {"id": len(self.notes) + 1, "owner": owner, "text": text}`; filter `self.notes` by owner.

</details>

<details><summary>Hint 2</summary>

Parameters look like `user: Annotated[str, Depends(current_user)]` and `page: Annotated[dict, Depends(pagination)]`.

</details>

<details><summary>Hint 3</summary>

In tests (and for you to try): `app.dependency_overrides[get_store] = lambda: NoteStore()` gives a fresh store.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_auth_required` | Raise HTTPException(401) with the WWW-Authenticate header when the key is missing or unknown. |
| `test_create_and_list_per_user` | Inject the user and store with Depends; return 201 for creation. |
| `test_pagination` | Declare the limit/offset constraints in the pagination dependency and slice the notes. |
| `test_override_isolates_global_store` | Endpoints must get the store through `Depends(get_store)` so tests can override it. |
| `test_yield_cleanup` | Append 'open', `yield` the list inside try, append 'close' in finally; append 'list' in the endpoint. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each concern — storage, authentication, paging, request logging — is a small function that
endpoints declare with `Depends`. FastAPI resolves them per request, validates their parameters
and runs the code after `yield` once the response is done. Because endpoints never reach for
globals directly, tests can substitute any dependency through `dependency_overrides`.

## References

- [FastAPI Tutorial: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) — FastAPI (Sebastián Ramírez) (`S076`)
- [FastAPI Advanced: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) — FastAPI (Sebastián Ramírez) (`S079`)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html) — Python Software Foundation (`S064`)
