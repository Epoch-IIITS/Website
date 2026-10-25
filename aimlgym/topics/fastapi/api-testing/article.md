# Testing an API

## Learning outcomes

After this lesson you can:

- Write unittest tests for an API with TestClient
- Cover success paths, status codes, validation, authentication and missing resources
- Keep tests independent by building a fresh app per test
- Judge test quality by whether broken versions of the API are caught

## Intuition
An API is a promise to its clients: these URLs, these status codes, these JSON shapes, these
errors. Tests are how you keep that promise while changing code. In PY-27 you tested a
function; here you test a whole application through HTTP — still in-process, still fast.

## Precise explanation
```python
from fastapi.testclient import TestClient

class ApiTests(unittest.TestCase):
    make_app = staticmethod(create_app)

    def setUp(self):
        self.client = TestClient(self.make_app())     # fresh app and state per test

    def test_create_returns_201(self):
        r = self.client.post("/notes", json={"title": "t", "body": "b"},
                             headers={"X-Token": "secret"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["title"], "t")
```
A thorough API suite checks, for each endpoint:
* the **success** status code and body shape;
* **validation**: invalid input gives 422;
* **authentication**: missing or wrong credentials give 401;
* **not found**: unknown ids give 404;
* **behaviour across requests**: what you create can be read back, ids are unique, lists are
  in the documented order.

Assert on status codes *and* bodies. Keep each test independent (new app in `setUp`), and use
dependency overrides or fakes (FA-13) instead of real external services.

## Worked example
Creating two notes and reading `GET /notes` should return both, oldest first, with ids 1 and 2 —
one test that catches broken id assignment *and* wrong ordering.

## Common mistakes
* Checking only `status_code == 200` for creation (should be 201).
* Sharing one app across tests, so test order changes results.
* Testing only the happy path, so a missing auth check ships unnoticed.

## Why this matters
These tests are what lets you refactor, upgrade FastAPI or add features without breaking clients.

## References

- [FastAPI Tutorial: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — FastAPI (Sebastián Ramírez) (`S078`)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html) — Python Software Foundation (`S002`)
- [FastAPI Advanced: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) — FastAPI (Sebastián Ramírez) (`S079`)
