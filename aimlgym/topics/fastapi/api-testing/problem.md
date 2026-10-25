# FA-15 · Testing an API

**Topic:** FastAPI · **Difficulty:** advanced · **Allowed packages:** fastapi

**Builds on:** FA-14 Async Endpoints and External Services, PY-27 Writing Unit Tests

Read the lesson first: [article.md](article.md)

## Task

The starter contains a correct `create_app()` for a notes API:

* `POST /notes` with header `X-Token: secret` and body `{"title": 1–100 characters, "body":
  string}` → 201 `{"id", "title", "body"}` (ids 1, 2, ...); wrong or missing token → 401;
  invalid body → 422.
* `GET /notes/{note_id}` → 200 note or 404.
* `GET /notes` → all notes in creation order.

Write `class ApiTests(unittest.TestCase)` with **at least six** tests. Get the app with
`self.make_app()` (class attribute `make_app = staticmethod(create_app)`); the grader replaces it.

Your tests must pass against the correct app, and each of these broken versions must fail at least
one of your tests: (1) creation returns 200 instead of 201, (2) the token is not checked,
(3) unknown ids return 200 with `null` instead of 404, (4) empty titles are accepted, (5) every
note gets id 1, (6) `GET /notes` returns newest first.

## Hints

<details><summary>Hint 1</summary>

One behaviour per test: 201 on create; 401 without the header; 404 for /notes/99; 422 for an empty title.

</details>

<details><summary>Hint 2</summary>

Create two notes and check the ids are 1 and 2 — that catches the 'every id is 1' bug.

</details>

<details><summary>Hint 3</summary>

Check that `GET /notes` returns titles in creation order after creating two notes.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_at_least_six_tests` | Add more `test_...` methods to ApiTests. |
| `test_pass_on_correct_app` | One of your expectations is wrong for the correct app; re-read the API description. |
| `test_catches_wrong_create_status` | Assert that creating a note returns status 201. |
| `test_catches_missing_token_check` | Send a request without the X-Token header and expect 401. |
| `test_catches_missing_404` | Request a note id that does not exist and expect 404. |
| `test_catches_empty_title` | Post an empty title and expect 422. |
| `test_catches_duplicate_ids` | Create two notes and check their ids differ (1 and 2). |
| `test_catches_wrong_order` | Create two notes and check GET /notes lists them oldest first. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each test targets one promise of the API — status codes, authentication, validation, missing
resources, id assignment and ordering — and builds its own app in `setUp`, so tests are
independent. Because every broken version violates one of those promises, each one fails at
least one test while the correct app passes them all.

## References

- [FastAPI Tutorial: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — FastAPI (Sebastián Ramírez) (`S078`)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html) — Python Software Foundation (`S002`)
- [FastAPI Advanced: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) — FastAPI (Sebastián Ramírez) (`S079`)
