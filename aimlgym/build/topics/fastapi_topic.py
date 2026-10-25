"""FastAPI topic, part 2: FastAPI applications tested in-process with fastapi.testclient.

Requires the `fastapi` package and `httpx` (used by TestClient). No server is started and no
network is used.
"""

PROBLEMS = [
# ---------------------------------------------------------------- fastapi-routes
{
"slug": "fastapi-routes", "title": "First FastAPI Routes",
"difficulty": "intermediate", "prereqs": ["asgi-app"], "packages": ["fastapi"],
"objectives": ["Create a FastAPI application and register path operations with decorators",
               "Declare typed path parameters and get automatic 422 errors",
               "Test an app in-process with TestClient",
               "Relate FastAPI's routing to the router you wrote by hand"],
"tags": ["fastapi", "routing", "path-parameters", "testclient", "openapi"],
"sources": ["S070", "S071", "S078"], "entry": "app (FastAPI); route_table(app)",
"article": r'''
# First FastAPI Routes

## Intuition
Everything from the first seven steps — parsing requests, choosing status codes, routing,
converting path parameters, speaking ASGI — is what FastAPI does for you. You write ordinary
Python functions with type hints; FastAPI turns them into an ASGI application, validates inputs
from the hints and documents the API automatically.

## Precise explanation
```python
from fastapi import FastAPI

app = FastAPI(title="Epoch Learn API")

@app.get("/items/{item_id}")          # method + path pattern, like Router.route
def read_item(item_id: int):           # the hint makes FastAPI convert and validate
    return {"item_id": item_id}       # dicts are returned as JSON with status 200
```
* `@app.get`, `@app.post`, `@app.put`, `@app.delete`, ... register **path operations**.
* `{item_id}` in the path becomes the parameter of the same name; `int` means `/items/abc` gets a
  **422** response with `loc: ["path", "item_id"]` — exactly what [[manual-router]] produced.
* Unknown paths → 404 and wrong methods → 405, automatically.
* Routes are matched in order: declare `/users/me` before `/users/{name}`.
* **Testing**: `TestClient(app)` (from `fastapi.testclient`, built on HTTPX) calls the ASGI app
  in-process: `client.get("/items/3").json()`. No server or network is involved — the same idea as
  [[asgi-app]]'s `call_asgi`.
* `app.openapi()` returns the OpenAPI schema FastAPI generated; a running server shows it as
  interactive docs at `/docs`.
* `app.routes` lists registered routes; path operations are `fastapi.routing.APIRoute` objects
  with `.path` and `.methods`.

To run a real server locally (optional): `pip install "fastapi[standard]"` and
`fastapi dev main.py`, then open `http://127.0.0.1:8000/docs`.

## Worked example
```python
from fastapi.testclient import TestClient
client = TestClient(app)
client.get("/items/21").json()       # {'item_id': 21}
client.get("/items/x").status_code   # 422
client.post("/items/21").status_code # 405
```

## Common mistakes
* Forgetting the type hint, so `item_id` arrives as a string.
* Declaring `/users/{name}` before `/users/me`, so `me` is treated as a name.
* Starting a real server inside tests instead of using `TestClient`.

## Why this matters
The following steps add query parameters, bodies, errors, response models, dependencies and
async endpoints to this same pattern.
''',
"statement": r'''
Create a module-level `app = FastAPI(title="Epoch Learn API")` with:

| Method | Path | Response |
|---|---|---|
| GET | `/` | `{"message": "Hello, Epoch Learn"}` |
| GET | `/health` | `{"status": "ok"}` |
| GET | `/users/me` | `{"user": "current"}` |
| GET | `/users/{name}` | `{"user": name}` |
| GET | `/items/{item_id}` (int) | `{"item_id": item_id, "double": 2 * item_id}` |
| DELETE | `/items/{item_id}` (int) | `{"deleted": item_id}` |

Also write `route_table(app)` → sorted list of `(method, path)` tuples for every `APIRoute`
in `app.routes` (one tuple per method).
''',
"starter": r'''
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
''',
"hints": [
    "`@app.get(\"/items/{item_id}\")` above `def read_item(item_id: int):`.",
    "Register `/users/me` before `/users/{name}`.",
    "`sorted((m, r.path) for r in app.routes if isinstance(r, APIRoute) for m in r.methods)`.",
],
"solution": r'''
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
''',
"explanation": r'''
Each decorator registers one path operation; type hints drive conversion and validation, so the
handlers contain only the response logic. Declaring the fixed `/users/me` route first keeps it
from being captured by the parameterised route. `route_table` reads the same registry FastAPI
uses for routing and for the OpenAPI schema.
''',
"tests": r'''
from fastapi.testclient import TestClient

client = TestClient(S.app)


class TestFirstRoutes(unittest.TestCase):
    def test_root_and_health(self):
        self.assertEqual(client.get("/").json(), {"message": "Hello, Epoch Learn"})
        self.assertEqual(client.get("/health").json(), {"status": "ok"})

    def test_typed_path_param(self):
        r = client.get("/items/21")
        self.assertEqual((r.status_code, r.json()), (200, {"item_id": 21, "double": 42}))

    def test_validation_422(self):
        r = client.get("/items/abc")
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json()["detail"][0]["loc"], ["path", "item_id"])

    def test_404_and_405(self):
        self.assertEqual(client.get("/nothing").status_code, 404)
        self.assertEqual(client.post("/items/1").status_code, 405)
        self.assertEqual(client.delete("/items/5").json(), {"deleted": 5})

    def test_route_order(self):
        self.assertEqual(client.get("/users/me").json(), {"user": "current"})
        self.assertEqual(client.get("/users/ada").json(), {"user": "ada"})

    def test_route_table_and_openapi(self):
        self.assertEqual(S.route_table(S.app), [
            ("DELETE", "/items/{item_id}"), ("GET", "/"), ("GET", "/health"),
            ("GET", "/items/{item_id}"), ("GET", "/users/me"), ("GET", "/users/{name}")])
        self.assertEqual(S.app.openapi()["info"]["title"], "Epoch Learn API")
        self.assertIn("/items/{item_id}", S.app.openapi()["paths"])
''',
"feedback": [
    ("test_typed_path_param", "Annotate `item_id: int` so FastAPI converts it."),
    ("test_validation_422", "With an `int` hint, FastAPI rejects 'abc' with 422 automatically — check the hint."),
    ("test_404_and_405", "Register GET and DELETE for /items/{item_id}; FastAPI answers other methods with 405."),
    ("test_route_order", "Declare `/users/me` before `/users/{name}`."),
    ("test_route_table_and_openapi", "Collect `(method, route.path)` for APIRoute objects and sort the list; set the app title."),
],
"library": {
"text": r'''
The test below runs the same requests through a copy of the hand-written router from
[[manual-router]] and through your FastAPI app, and checks they produce the same status codes and
bodies. The difference is what you no longer write: segment matching, conversions, 404/405/422
decisions, JSON encoding and documentation.
''',
"tests": r'''
class MiniRouter:
    def __init__(self):
        self.routes = []

    def add(self, method, pattern, handler):
        self.routes.append((method, pattern.strip("/").split("/"), handler))

    def dispatch(self, method, path):
        parts = path.strip("/").split("/")
        found = []
        for m, segs, h in self.routes:
            if len(segs) == len(parts) and all(s.startswith("{") or s == p for s, p in zip(segs, parts)):
                found.append((m, segs, h))
        if not found:
            return 404, None
        chosen = [(segs, h) for m, segs, h in found if m == method]
        if not chosen:
            return 405, None
        segs, h = chosen[0]
        kwargs = {}
        for s, p in zip(segs, parts):
            if s.startswith("{"):
                name, _, conv = s[1:-1].partition(":")
                if conv == "int":
                    if not p.lstrip("-").isdigit():
                        return 422, None
                    p = int(p)
                kwargs[name] = p
        return 200, h(**kwargs)


def manual_app():
    r = MiniRouter()
    r.add("GET", "/", lambda: {"message": "Hello, Epoch Learn"})
    r.add("GET", "/health", lambda: {"status": "ok"})
    r.add("GET", "/users/me", lambda: {"user": "current"})
    r.add("GET", "/users/{name}", lambda name: {"user": name})
    r.add("GET", "/items/{item_id:int}", lambda item_id: {"item_id": item_id, "double": 2 * item_id})
    r.add("DELETE", "/items/{item_id:int}", lambda item_id: {"deleted": item_id})
    return r


class TestAgainstManualRouter(unittest.TestCase):
    def test_same_behaviour(self):
        manual = manual_app()
        for method, path in [("GET", "/"), ("GET", "/users/me"), ("GET", "/users/bo"), ("GET", "/items/7"),
                             ("DELETE", "/items/7"), ("GET", "/items/x"), ("PUT", "/items/7"), ("GET", "/missing")]:
            status, body = manual.dispatch(method, path)
            r = client.request(method, path)
            self.assertEqual(r.status_code, status, (method, path))
            if status == 200:
                self.assertEqual(r.json(), body)
''',
},
},
# ---------------------------------------------------------------- fastapi-params
{
"slug": "fastapi-params", "title": "Query and Path Parameters with Validation",
"difficulty": "intermediate", "prereqs": ["fastapi-routes"], "packages": ["fastapi"],
"objectives": ["Declare optional and required query parameters with defaults",
               "Add constraints with Annotated, Query and Path",
               "Restrict a parameter to fixed choices with an Enum",
               "Accept repeated query parameters as a list"],
"tags": ["fastapi", "query-parameters", "validation", "annotated", "enum"],
"sources": ["S072", "S071", "S078"], "entry": "app (FastAPI) with GET /books, /books/by-year/{year}, /books/tagged",
"article": r'''
# Query and Path Parameters with Validation

## Intuition
`GET /books?q=learning&limit=2&order=desc` asks for a filtered, sorted page of results. In
[[urls-query]] you decoded such strings by hand; FastAPI reads each function parameter that is not
in the path from the query string, converts it using its type hint, and enforces any limits you
declare.

## Precise explanation
```python
from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Path, Query

class Order(str, Enum):              # allowed values only: "asc" or "desc"
    asc = "asc"
    desc = "desc"

@app.get("/books")
def list_books(
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,  # optional
    limit: Annotated[int, Query(ge=1, le=5)] = 3,                          # default 3, 1..5
    offset: Annotated[int, Query(ge=0)] = 0,
    order: Order = Order.asc,
): ...
```
* A parameter **with a default** is optional; one without a default is required (missing → 422).
* `Annotated[type, Query(...)]` attaches validation (`ge`, `le`, `gt`, `lt` for numbers;
  `min_length`, `max_length`, `pattern` for strings). `Path(...)` does the same for path
  parameters. `Annotated` comes from `typing` and keeps the plain type visible.
* `str | None` means "a string or nothing".
* An `Enum` subclass of `str` limits values to its members; `order.value` is the string.
* `tag: Annotated[list[str], Query()] = []` collects `?tag=a&tag=b` into `["a", "b"]`.
* Every violation produces 422 with `loc` such as `["query", "limit"]`.

## Worked example
`GET /books?limit=9` → 422 because 9 > 5; `GET /books?order=random` → 422 (not an Order);
`GET /books?q=deep&order=desc` → books whose title contains "deep", newest first.

## Common mistakes
* Using a mutable default list outside `Query` in older styles; with `Annotated` the default
  `[]` is safe because FastAPI copies it.
* Forgetting that query values arrive as strings and relying on manual `int()` calls.
* Validating limits inside the function instead of declaring them, which hides them from the docs.

## Why this matters
Declared constraints appear in the OpenAPI schema, so clients can see the rules, and invalid
requests never reach your code.
''',
"statement": r'''
The starter defines `BOOKS`, a list of six dicts with `id`, `title`, `year` and `tags`, and
`app = FastAPI()`. Implement:

1. `GET /books` with parameters `q` (optional, 2–50 characters), `limit` (1–5, default 3),
   `offset` (≥ 0, default 0) and `order` (`asc`/`desc` Enum, default `asc`). Filter by
   case-insensitive substring `q` in the title, sort by `(year, id)` ascending or descending,
   and return `{"count": <number of matches>, "items": <the page of matching books>}`.
2. `GET /books/by-year/{year}` with `year` between 1900 and 2100 (`Path`) → list of titles from
   that year in id order (possibly empty).
3. `GET /books/tagged` with a repeated query parameter `tag` (default empty list) → ids of books
   that have **all** the given tags, in id order.
''',
"starter": r'''
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query

BOOKS = [
    {"id": 1, "title": "Deep Learning", "year": 2016, "tags": ["dl", "ml"]},
    {"id": 2, "title": "Pattern Recognition and Machine Learning", "year": 2006, "tags": ["ml", "stats"]},
    {"id": 3, "title": "Reinforcement Learning", "year": 2018, "tags": ["rl", "ml"]},
    {"id": 4, "title": "Speech and Language Processing", "year": 2024, "tags": ["nlp"]},
    {"id": 5, "title": "Dive into Deep Learning", "year": 2023, "tags": ["dl", "ml"]},
    {"id": 6, "title": "Think Stats", "year": 2014, "tags": ["stats"]},
]

app = FastAPI()


@app.get("/books")
def list_books(q: str | None = None, limit: int = 3, offset: int = 0):
    # TODO: validation, Enum order, filtering, sorting, paging
    return {"count": len(BOOKS), "items": BOOKS[:limit]}


# TODO: /books/by-year/{year} and /books/tagged
''',
"hints": [
    "`class Order(str, Enum): asc = \"asc\"; desc = \"desc\"` and the parameter `order: Order = Order.asc`.",
    "`limit: Annotated[int, Query(ge=1, le=5)] = 3`; `year: Annotated[int, Path(ge=1900, le=2100)]`.",
    "`sorted(matches, key=lambda b: (b[\"year\"], b[\"id\"]), reverse=order == Order.desc)`; tags: `tag: Annotated[list[str], Query()] = []` and `set(tag) <= set(b[\"tags\"])`.",
],
"solution": r'''
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query

BOOKS = [
    {"id": 1, "title": "Deep Learning", "year": 2016, "tags": ["dl", "ml"]},
    {"id": 2, "title": "Pattern Recognition and Machine Learning", "year": 2006, "tags": ["ml", "stats"]},
    {"id": 3, "title": "Reinforcement Learning", "year": 2018, "tags": ["rl", "ml"]},
    {"id": 4, "title": "Speech and Language Processing", "year": 2024, "tags": ["nlp"]},
    {"id": 5, "title": "Dive into Deep Learning", "year": 2023, "tags": ["dl", "ml"]},
    {"id": 6, "title": "Think Stats", "year": 2014, "tags": ["stats"]},
]

app = FastAPI()


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


@app.get("/books")
def list_books(
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=5)] = 3,
    offset: Annotated[int, Query(ge=0)] = 0,
    order: Order = Order.asc,
):
    matches = [b for b in BOOKS if q is None or q.lower() in b["title"].lower()]
    matches = sorted(matches, key=lambda b: (b["year"], b["id"]), reverse=order == Order.desc)
    return {"count": len(matches), "items": matches[offset:offset + limit]}


@app.get("/books/by-year/{year}")
def books_by_year(year: Annotated[int, Path(ge=1900, le=2100)]):
    return [b["title"] for b in BOOKS if b["year"] == year]


@app.get("/books/tagged")
def books_tagged(tag: Annotated[list[str], Query()] = []):
    wanted = set(tag)
    return [b["id"] for b in BOOKS if wanted <= set(b["tags"])]
''',
"explanation": r'''
All validation is declared in the signatures, so the bodies only filter, sort and slice. The Enum
restricts `order` to two strings, `Path` bounds the year, and the list-typed query parameter
collects repeated `tag` values. FastAPI produces 422 responses for every rule violation before the
function runs.
''',
"tests": r'''
from fastapi.testclient import TestClient

client = TestClient(S.app)


def ids(resp):
    return [b["id"] for b in resp.json()["items"]]


class TestParams(unittest.TestCase):
    def test_defaults(self):
        r = client.get("/books")
        self.assertEqual((r.json()["count"], ids(r)), (6, [2, 6, 1]))

    def test_filter_sort_page(self):
        r = client.get("/books", params={"q": "DEEP", "order": "desc"})
        self.assertEqual((r.json()["count"], ids(r)), (2, [5, 1]))
        r = client.get("/books", params={"limit": 2, "offset": 2})
        self.assertEqual(ids(r), [1, 3])

    def test_limits_validated(self):
        for params, field in [({"limit": 9}, "limit"), ({"limit": 0}, "limit"), ({"offset": -1}, "offset"),
                              ({"q": "x"}, "q"), ({"order": "random"}, "order")]:
            r = client.get("/books", params=params)
            self.assertEqual(r.status_code, 422, params)
            self.assertEqual(r.json()["detail"][0]["loc"], ["query", field])

    def test_by_year(self):
        self.assertEqual(client.get("/books/by-year/2016").json(), ["Deep Learning"])
        self.assertEqual(client.get("/books/by-year/2000").json(), [])
        self.assertEqual(client.get("/books/by-year/1800").status_code, 422)

    def test_tagged(self):
        self.assertEqual(client.get("/books/tagged", params=[("tag", "ml"), ("tag", "dl")]).json(), [1, 5])
        self.assertEqual(client.get("/books/tagged", params={"tag": "stats"}).json(), [2, 6])
        self.assertEqual(client.get("/books/tagged").json(), [1, 2, 3, 4, 5, 6])

    def test_documented_in_openapi(self):
        params = {p["name"]: p for p in S.app.openapi()["paths"]["/books"]["get"]["parameters"]}
        self.assertEqual(params["limit"]["schema"]["maximum"], 5)
        self.assertEqual(sorted(params), ["limit", "offset", "order", "q"])
''',
"feedback": [
    ("test_defaults", "Sort by (year, id) ascending by default and return 3 items."),
    ("test_filter_sort_page", "Filter case-insensitively, reverse the sort for desc, then slice `[offset:offset + limit]`."),
    ("test_limits_validated", "Declare the constraints with `Annotated[..., Query(...)]` and use an Enum for order."),
    ("test_by_year", "Use `Annotated[int, Path(ge=1900, le=2100)]` for the year."),
    ("test_tagged", "Declare `tag: Annotated[list[str], Query()] = []` and keep books whose tags include all of them."),
    ("test_documented_in_openapi", "Constraints declared with Query appear in the OpenAPI schema."),
],
},
# ---------------------------------------------------------------- pydantic-bodies
{
"slug": "pydantic-bodies", "title": "Request Bodies with Pydantic",
"difficulty": "intermediate", "prereqs": ["fastapi-params", "json-bodies"], "packages": ["fastapi"],
"objectives": ["Describe a JSON body as a Pydantic model with typed, constrained fields",
               "Forbid unknown fields and choose strict types where coercion would hide errors",
               "Receive a validated model in a POST endpoint",
               "Compare Pydantic validation with the hand-written validator"],
"tags": ["pydantic", "request-body", "validation", "basemodel", "fastapi"],
"sources": ["S080", "S073"], "entry": "class Item(BaseModel); parse_item(data); app with POST /items",
"article": r'''
# Request Bodies with Pydantic

## Intuition
In [[json-bodies]] you wrote forty lines to check a name, a price and some tags. **Pydantic**
lets you declare the same rules as a class with type hints; FastAPI reads the body, validates it
against the class and hands your function a ready-made object — or replies 422 with every error.

## Precise explanation
```python
from pydantic import BaseModel, ConfigDict, Field

class Item(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(ge=0, strict=True)
    tags: list[str] = []
    quantity: int = Field(default=0, ge=0, strict=True)

@app.post("/items")
def create_item(item: Item):        # a model-typed parameter is read from the JSON body
    return {"item": item.model_dump(), "total": item.price * item.quantity}
```
* Fields without defaults are required. `Field(...)` adds constraints; `list[str]` validates
  every element.
* **Lax vs strict**: by default Pydantic *coerces* — `"3"` and `True` become `3.0` for a float.
  That is convenient for query strings but can hide client bugs in JSON, so `strict=True`
  rejects them (an `int` is still accepted for a `float`).
* `extra="forbid"` rejects unknown fields; `str_strip_whitespace=True` strips strings before
  checking `min_length`.
* `Item.model_validate(data)` validates a dict outside FastAPI and raises
  `pydantic.ValidationError`; `.errors()` lists `loc`, `msg` and `type` for each problem.
* `item.model_dump()` turns the model back into a dict.

## Worked example
`{"name": "  pen ", "price": 2}` → `Item(name="pen", price=2.0, tags=[], quantity=0)`.
`{"name": "", "price": "3", "colour": "red"}` → three errors: name too short, price not a float,
extra field `colour`.

## Common mistakes
* Assuming Pydantic rejects `"3"` for a number — only in strict mode.
* Using mutable defaults in plain classes; Pydantic copies field defaults safely.
* Reading `await request.json()` manually instead of declaring a model.

## Why this matters
Models are the API's contract: they validate input, shape output ([[response-models]]) and
generate the JSON Schema shown in the docs.
''',
"statement": r'''
1. Define `class Item(BaseModel)` exactly as in the lesson (fields `name`, `price`, `tags`,
   `quantity`, with `extra="forbid"` and `str_strip_whitespace=True`).
2. `parse_item(data)` → `Item.model_validate(data)` (let `ValidationError` propagate).
3. `app = FastAPI()` with `POST /items` returning
   `{"item": item.model_dump(), "total": item.price * item.quantity}`.
''',
"starter": r'''
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    name: str
    price: float
    # TODO: constraints, tags, quantity, model_config


def parse_item(data):
    # TODO
    return Item(**data)


app = FastAPI()

# TODO: POST /items
''',
"hints": [
    "`model_config = ConfigDict(extra=\"forbid\", str_strip_whitespace=True)` goes in the class body.",
    "`price: float = Field(ge=0, strict=True)` and `quantity: int = Field(default=0, ge=0, strict=True)`.",
    "`@app.post(\"/items\")` above `def create_item(item: Item):`.",
],
"solution": r'''
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(ge=0, strict=True)
    tags: list[str] = []
    quantity: int = Field(default=0, ge=0, strict=True)


def parse_item(data):
    return Item.model_validate(data)


app = FastAPI()


@app.post("/items")
def create_item(item: Item):
    return {"item": item.model_dump(), "total": item.price * item.quantity}
''',
"explanation": r'''
The model states every rule declaratively; strict numeric fields and `extra="forbid"` reproduce
the hand-written validator's behaviour, and whitespace stripping happens before the length check.
FastAPI validates the body against the model and passes a typed object to the endpoint.
''',
"tests": r'''
from fastapi.testclient import TestClient
from pydantic import ValidationError

client = TestClient(S.app)


class TestPydanticBodies(unittest.TestCase):
    def test_parse_and_defaults(self):
        item = S.parse_item({"name": "  pen ", "price": 2})
        self.assertEqual(item.model_dump(), {"name": "pen", "price": 2.0, "tags": [], "quantity": 0})

    def test_errors_listed(self):
        with self.assertRaises(ValidationError) as ctx:
            S.parse_item({"name": " ", "price": "3", "colour": "red"})
        self.assertEqual(sorted(e["loc"] for e in ctx.exception.errors()), [("colour",), ("name",), ("price",)])

    def test_strict_types(self):
        for bad in ({"name": "a", "price": True}, {"name": "a", "price": 1, "quantity": 1.5},
                    {"name": "a", "price": 1, "tags": ["x", 3]}, {"name": "a" * 51, "price": 1}):
            with self.assertRaises(ValidationError, msg=bad):
                S.parse_item(bad)

    def test_post_ok(self):
        r = client.post("/items", json={"name": "ink", "price": 1.5, "quantity": 4, "tags": ["blue"]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"item": {"name": "ink", "price": 1.5, "tags": ["blue"], "quantity": 4}, "total": 6.0})

    def test_post_422(self):
        r = client.post("/items", json={"price": -1})
        self.assertEqual(r.status_code, 422)
        self.assertEqual(sorted(tuple(e["loc"]) for e in r.json()["detail"]), [("body", "name"), ("body", "price")])

    def test_schema(self):
        schema = S.Item.model_json_schema()
        self.assertEqual(schema["required"], ["name", "price"])
        self.assertFalse(schema["additionalProperties"])
''',
"feedback": [
    ("test_parse_and_defaults", "Strip whitespace via model_config and give tags and quantity defaults."),
    ("test_errors_listed", "Use `extra=\"forbid\"`, `min_length=1` on name and a strict float price."),
    ("test_strict_types", "Strict numbers reject booleans and floats for ints; list[str] checks every tag; limit name to 50 characters."),
    ("test_post_ok", "The endpoint takes `item: Item` and returns the dumped model and price * quantity."),
    ("test_post_422", "FastAPI reports body errors with loc ['body', field] when the model is the only body parameter."),
],
"library": {
"text": r'''
The test below runs the hand-written rules from [[json-bodies]] (extended with `quantity`) and
your Pydantic model over the same payloads and checks that they accept and reject exactly the same
ones. Pydantic also gives you error types, JSON Schema, serialisation and FastAPI integration for
free.
''',
"tests": r'''
def manual_ok(data):
    if not isinstance(data, dict) or set(data) - {"name", "price", "tags", "quantity"}:
        return False
    name, price = data.get("name"), data.get("price")
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 50:
        return False
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return False
    tags = data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        return False
    q = data.get("quantity", 0)
    return isinstance(q, int) and not isinstance(q, bool) and q >= 0


def pydantic_ok(data):
    try:
        S.parse_item(data)
        return True
    except ValidationError:
        return False


class TestAgainstManualValidator(unittest.TestCase):
    def test_same_decisions(self):
        payloads = [{"name": "a", "price": 0}, {"name": " a ", "price": 2.5, "tags": []}, {"name": "", "price": 1},
                    {"name": "a", "price": -0.1}, {"name": "a", "price": "1"}, {"name": "a", "price": False},
                    {"name": "a", "price": 1, "quantity": -1}, {"name": "a", "price": 1, "quantity": 2},
                    {"name": "a", "price": 1, "extra": None}, {"price": 1}, {"name": 3, "price": 1},
                    {"name": "a", "price": 1, "tags": "ml"}]
        for p in payloads:
            self.assertEqual(pydantic_ok(p), manual_ok(p), p)
''',
},
},
# ---------------------------------------------------------------- fastapi-errors
{
"slug": "fastapi-errors", "title": "Handling Errors in FastAPI",
"difficulty": "intermediate", "prereqs": ["pydantic-bodies"], "packages": ["fastapi"],
"objectives": ["Raise HTTPException with a status code, detail and headers",
               "Turn domain exceptions into responses with exception handlers",
               "Customise the validation-error response",
               "Build apps with a factory so every test starts from fresh state"],
"tags": ["fastapi", "errors", "httpexception", "exception-handlers", "app-factory"],
"sources": ["S074", "S066"], "entry": "class OutOfStock(Exception); create_app()",
"article": r'''
# Handling Errors in FastAPI

## Intuition
A good API fails *predictably*: the client gets the right status code and a body it can act on.
FastAPI gives you two tools — raise `HTTPException` where the problem is detected, or raise your
own domain exception and convert it to a response in one central **exception handler**.

## Precise explanation
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "missing"})
# → 404 {"detail": "Item not found"} with the extra header

class OutOfStock(Exception):            # a domain error, independent of HTTP
    def __init__(self, item, requested, available): ...

@app.exception_handler(OutOfStock)
async def out_of_stock(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=409, content={"error": "out_of_stock", ...})
```
* Business code raises `OutOfStock`; only the handler knows it means 409. The same exception can
  be reused outside the web layer.
* `RequestValidationError` is what FastAPI raises for 422s. Registering a handler for it changes
  the error format for the whole app; `exc.errors()` gives the usual list of `loc`/`msg`.
* Handlers are `async def` functions taking `(request, exc)` ([[asyncio-basics]]).
* **App factory**: `def create_app(): app = FastAPI(); ... return app`. State such as stock
  levels lives inside the factory, so each test builds a fresh app and tests cannot affect each
  other.

## Worked example
Stock `{1: pen (3 left), 2: ink (0 left)}`: `POST /items/2/buy?qty=1` raises `OutOfStock` → 409
`{"error": "out_of_stock", "item": "ink", "requested": 1, "available": 0}`.
`POST /items/1/buy?qty=0` → 422 `{"error": "validation_error", "fields": ["query.qty"]}`.

## Common mistakes
* Returning `{"error": ...}` with status 200.
* Catching every `Exception` in a handler and hiding programming errors as 400s.
* Using module-level state, so the order of tests changes the results.

## Why this matters
Consistent error bodies let clients (and agents calling your API as a tool) recover
automatically, as in [[validate-and-retry]].
''',
"statement": r'''
Define `class OutOfStock(Exception)` storing `item`, `requested` and `available`, and
`create_app()` returning a new `FastAPI` app with its own stock dict
`{1: {"name": "pen", "stock": 3}, 2: {"name": "ink", "stock": 0}}`:

* `GET /items/{item_id}` (int) → `{"id", "name", "stock"}`; unknown id → `HTTPException(404,
  detail="Item not found", headers={"X-Error": "missing"})`.
* `POST /items/{item_id}/buy` with query `qty` (int, ≥ 1, default 1): unknown id → same 404;
  `qty` larger than the stock → raise `OutOfStock`; otherwise subtract and return
  `{"item": name, "remaining": stock}`.
* Handler for `OutOfStock` → 409 `{"error": "out_of_stock", "item", "requested", "available"}`.
* Handler for `RequestValidationError` → 422 `{"error": "validation_error", "fields": [...]}` where
  each field is the error's `loc` joined with `"."` (e.g. `"path.item_id"`), in FastAPI's order.
''',
"starter": r'''
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class OutOfStock(Exception):
    def __init__(self, item, requested, available):
        super().__init__(f"{item}: requested {requested}, available {available}")
        self.item, self.requested, self.available = item, requested, available


def create_app():
    app = FastAPI()
    stock = {1: {"name": "pen", "stock": 3}, 2: {"name": "ink", "stock": 0}}

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        # TODO: 404 for unknown ids
        return {"id": item_id, **stock[item_id]}

    # TODO: POST /items/{item_id}/buy and the two exception handlers
    return app
''',
"hints": [
    "`if item_id not in stock: raise HTTPException(status_code=404, detail=\"Item not found\", headers={\"X-Error\": \"missing\"})`.",
    "Declare `qty: Annotated[int, Query(ge=1)] = 1`; raise `OutOfStock(name, qty, available)` when `qty > available`.",
    "`@app.exception_handler(RequestValidationError)` with `fields = [\".\".join(str(p) for p in e[\"loc\"]) for e in exc.errors()]`.",
],
"solution": r'''
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class OutOfStock(Exception):
    def __init__(self, item, requested, available):
        super().__init__(f"{item}: requested {requested}, available {available}")
        self.item, self.requested, self.available = item, requested, available


def create_app():
    app = FastAPI()
    stock = {1: {"name": "pen", "stock": 3}, 2: {"name": "ink", "stock": 0}}

    def find(item_id):
        if item_id not in stock:
            raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "missing"})
        return stock[item_id]

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"id": item_id, **find(item_id)}

    @app.post("/items/{item_id}/buy")
    def buy(item_id: int, qty: Annotated[int, Query(ge=1)] = 1):
        entry = find(item_id)
        if qty > entry["stock"]:
            raise OutOfStock(entry["name"], qty, entry["stock"])
        entry["stock"] -= qty
        return {"item": entry["name"], "remaining": entry["stock"]}

    @app.exception_handler(OutOfStock)
    async def out_of_stock(request: Request, exc: OutOfStock):
        return JSONResponse(status_code=409, content={"error": "out_of_stock", "item": exc.item,
                                                      "requested": exc.requested, "available": exc.available})

    @app.exception_handler(RequestValidationError)
    async def validation(request: Request, exc: RequestValidationError):
        fields = [".".join(str(p) for p in e["loc"]) for e in exc.errors()]
        return JSONResponse(status_code=422, content={"error": "validation_error", "fields": fields})

    return app
''',
"explanation": r'''
A shared `find` helper raises the 404 in one place. The purchase logic raises a domain exception
that knows nothing about HTTP, and the handler maps it to 409 with a structured body. Overriding
the validation handler changes every 422 in the app. Because the stock dict lives inside the
factory, each `create_app()` call starts from the same state.
''',
"tests": r'''
from fastapi.testclient import TestClient


class TestErrors(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(S.create_app())

    def test_read_ok_and_404(self):
        self.assertEqual(self.client.get("/items/1").json(), {"id": 1, "name": "pen", "stock": 3})
        r = self.client.get("/items/9")
        self.assertEqual((r.status_code, r.json(), r.headers["x-error"]), (404, {"detail": "Item not found"}, "missing"))

    def test_buy_reduces_stock(self):
        self.assertEqual(self.client.post("/items/1/buy", params={"qty": 2}).json(), {"item": "pen", "remaining": 1})
        self.assertEqual(self.client.get("/items/1").json()["stock"], 1)
        self.assertEqual(self.client.post("/items/1/buy").json(), {"item": "pen", "remaining": 0})

    def test_out_of_stock_409(self):
        r = self.client.post("/items/2/buy")
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json(), {"error": "out_of_stock", "item": "ink", "requested": 1, "available": 0})
        r = self.client.post("/items/1/buy", params={"qty": 5})
        self.assertEqual(r.json()["available"], 3)
        self.assertEqual(self.client.get("/items/1").json()["stock"], 3)

    def test_buy_unknown_404(self):
        self.assertEqual(self.client.post("/items/7/buy").status_code, 404)

    def test_validation_format(self):
        r = self.client.post("/items/abc/buy", params={"qty": 0})
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json(), {"error": "validation_error", "fields": ["path.item_id", "query.qty"]})

    def test_fresh_state_per_app(self):
        self.client.post("/items/1/buy", params={"qty": 3})
        fresh = TestClient(S.create_app())
        self.assertEqual(fresh.get("/items/1").json()["stock"], 3)

    def test_exception_is_plain_python(self):
        e = S.OutOfStock("pen", 5, 3)
        self.assertEqual((e.item, e.requested, e.available), ("pen", 5, 3))
        self.assertIsInstance(e, Exception)
''',
"feedback": [
    ("test_read_ok_and_404", "Raise HTTPException(404, detail=..., headers={\"X-Error\": \"missing\"}) for unknown ids."),
    ("test_buy_reduces_stock", "Subtract qty from the stored stock and default qty to 1."),
    ("test_out_of_stock_409", "Raise OutOfStock before changing stock and map it to 409 in an exception handler."),
    ("test_validation_format", "Register a RequestValidationError handler that joins each loc with '.'."),
    ("test_fresh_state_per_app", "Create the stock dict inside create_app, not at module level."),
],
},
# ---------------------------------------------------------------- response-models
{
"slug": "response-models", "title": "Response Models and Status Codes",
"difficulty": "advanced", "prereqs": ["fastapi-errors"], "packages": ["fastapi"],
"objectives": ["Separate input and output models so secrets never leave the API",
               "Set success status codes such as 201 and 204",
               "Return lists of models and handle conflicts with 409",
               "Store a password hash instead of the password"],
"tags": ["fastapi", "response-model", "status-codes", "crud", "security"],
"sources": ["S075", "S070", "S066"], "entry": "class UserIn; class UserOut; create_app()",
"article": r'''
# Response Models and Status Codes

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
* `pattern=` validates strings with a regular expression ([[regex-text]]).
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
''',
"statement": r'''
Define `UserIn` and `UserOut` as in the lesson and `create_app()` with an in-memory store (ids
start at 1 and are never reused):

* `POST /users` → 201 `UserOut`; store `{"id", "username", "email", "password_hash"}` with
  `hashlib.sha256(password.encode()).hexdigest()`; an existing username → 409 `{"detail":
  "Username taken"}`.
* `GET /users` → list of `UserOut` in id order.
* `GET /users/{user_id}` → `UserOut` or 404 `{"detail": "User not found"}`.
* `DELETE /users/{user_id}` → 204 with an empty body, or 404.

Endpoints should return the stored dicts; the response model must remove `password_hash`.
''',
"starter": r'''
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
''',
"hints": [
    "Add `response_model=UserOut, status_code=201` to the POST decorator and store `password_hash` instead of `password`.",
    "Keep a counter (e.g. `state = {\"next_id\": 1}`) so deleted ids are not reused; check for an existing username first.",
    "`@app.delete(\"/users/{user_id}\", status_code=204)` and return `None`; `response_model=list[UserOut]` for the list.",
],
"solution": r'''
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
''',
"explanation": r'''
Input and output are different models, and every endpoint declares its response model, so the
stored `password_hash` is filtered out automatically. Status codes are declared on the decorators;
conflicts and missing users raise `HTTPException`. A separate id counter guarantees ids are never
reused after deletions.
''',
"tests": r'''
import hashlib

from fastapi.testclient import TestClient

ADA = {"username": "ada", "email": "ada@x.org", "password": "correct horse"}


class TestResponseModels(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(S.create_app())

    def test_create_201_without_secrets(self):
        r = self.client.post("/users", json=ADA)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json(), {"id": 1, "username": "ada", "email": "ada@x.org"})
        self.assertNotIn("password", r.text)
        self.assertNotIn(hashlib.sha256(b"correct horse").hexdigest(), r.text)

    def test_input_validation(self):
        for bad in ({**ADA, "username": "Ada!"}, {**ADA, "username": "ab"}, {**ADA, "password": "short"},
                    {**ADA, "email": "nope"}):
            self.assertEqual(self.client.post("/users", json=bad).status_code, 422, bad)

    def test_duplicate_409(self):
        self.client.post("/users", json=ADA)
        r = self.client.post("/users", json={**ADA, "email": "other@x.org"})
        self.assertEqual((r.status_code, r.json()), (409, {"detail": "Username taken"}))

    def test_list_and_read(self):
        self.client.post("/users", json=ADA)
        self.client.post("/users", json={**ADA, "username": "bob"})
        self.assertEqual([u["username"] for u in self.client.get("/users").json()], ["ada", "bob"])
        self.assertEqual(self.client.get("/users/2").json()["username"], "bob")
        self.assertNotIn("password_hash", self.client.get("/users").text)
        self.assertEqual(self.client.get("/users/9").status_code, 404)

    def test_delete_204_and_no_reuse(self):
        self.client.post("/users", json=ADA)
        r = self.client.delete("/users/1")
        self.assertEqual((r.status_code, r.content), (204, b""))
        self.assertEqual(self.client.get("/users/1").status_code, 404)
        self.assertEqual(self.client.delete("/users/1").status_code, 404)
        self.assertEqual(self.client.post("/users", json=ADA).json()["id"], 2)

    def test_openapi_response_schema(self):
        app = S.create_app()
        schema = app.openapi()["components"]["schemas"]
        self.assertNotIn("password", schema["UserOut"]["properties"])
        self.assertIn("201", app.openapi()["paths"]["/users"]["post"]["responses"])
''',
"feedback": [
    ("test_create_201_without_secrets", "Use `response_model=UserOut` and `status_code=201`, and never store the raw password."),
    ("test_input_validation", "Add the username pattern and length limits, the email pattern and an 8-character password minimum."),
    ("test_duplicate_409", "Check for an existing username before creating and raise HTTPException(409)."),
    ("test_list_and_read", "Use `response_model=list[UserOut]` for the list and return 404 for unknown ids."),
    ("test_delete_204_and_no_reuse", "Declare `status_code=204`, return None, and keep a separate id counter."),
],
},
# ---------------------------------------------------------------- fastapi-dependencies
{
"slug": "fastapi-dependencies", "title": "Dependencies and Dependency Overrides",
"difficulty": "advanced", "prereqs": ["response-models"], "packages": ["fastapi"],
"objectives": ["Share setup code between endpoints with Depends",
               "Authenticate with an API-key header dependency that raises 401",
               "Write dependencies with cleanup using yield",
               "Replace dependencies in tests with app.dependency_overrides"],
"tags": ["fastapi", "dependency-injection", "authentication", "testing", "overrides"],
"sources": ["S076", "S079", "S064"], "entry": "class NoteStore; get_store(); current_user(); pagination(); request_log(); create_app()",
"article": r'''
# Dependencies and Dependency Overrides

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
  credentials ([[unit-testing]]'s fakes, applied to an API).
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
Dependencies keep endpoints small and testable; [[fastapi-async]] uses an overridable dependency
to replace a slow external service with a fake.
''',
"statement": r'''
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
''',
"starter": r'''
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field


class NoteStore:
    def __init__(self):
        self.notes = []

    def add(self, owner, text):
        # TODO
        return {}

    def for_owner(self, owner):
        # TODO
        return []


STORE = NoteStore()
API_KEYS = {"key-ada": "ada", "key-bob": "bob"}
EVENTS = []


def get_store():
    return STORE


def current_user(x_api_key: Annotated[str | None, Header()] = None):
    # TODO: 401 for missing or unknown keys
    return "ada"


def pagination(limit: int = 10, offset: int = 0):
    # TODO: constraints
    return {"limit": limit, "offset": offset}


def request_log():
    # TODO: yield with cleanup
    return EVENTS


class NoteIn(BaseModel):
    text: str = Field(min_length=1)


def create_app():
    app = FastAPI()
    # TODO: POST /notes and GET /notes with Depends
    return app
''',
"hints": [
    "`note = {\"id\": len(self.notes) + 1, \"owner\": owner, \"text\": text}`; filter `self.notes` by owner.",
    "Parameters look like `user: Annotated[str, Depends(current_user)]` and `page: Annotated[dict, Depends(pagination)]`.",
    "In tests (and for you to try): `app.dependency_overrides[get_store] = lambda: NoteStore()` gives a fresh store.",
],
"solution": r'''
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field


class NoteStore:
    def __init__(self):
        self.notes = []

    def add(self, owner, text):
        note = {"id": len(self.notes) + 1, "owner": owner, "text": text}
        self.notes.append(note)
        return note

    def for_owner(self, owner):
        return [n for n in self.notes if n["owner"] == owner]


STORE = NoteStore()
API_KEYS = {"key-ada": "ada", "key-bob": "bob"}
EVENTS = []


def get_store():
    return STORE


def current_user(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key", headers={"WWW-Authenticate": "ApiKey"})
    return API_KEYS[x_api_key]


def pagination(limit: Annotated[int, Query(ge=1, le=50)] = 10,
               offset: Annotated[int, Query(ge=0)] = 0):
    return {"limit": limit, "offset": offset}


def request_log():
    EVENTS.append("open")
    try:
        yield EVENTS
    finally:
        EVENTS.append("close")


class NoteIn(BaseModel):
    text: str = Field(min_length=1)


def create_app():
    app = FastAPI()

    @app.post("/notes", status_code=201)
    def create_note(note: NoteIn,
                    user: Annotated[str, Depends(current_user)],
                    store: Annotated[NoteStore, Depends(get_store)]):
        return store.add(user, note.text)

    @app.get("/notes")
    def list_notes(user: Annotated[str, Depends(current_user)],
                   store: Annotated[NoteStore, Depends(get_store)],
                   page: Annotated[dict, Depends(pagination)],
                   log: Annotated[list, Depends(request_log)]):
        log.append("list")
        notes = store.for_owner(user)
        return notes[page["offset"]:page["offset"] + page["limit"]]

    return app
''',
"explanation": r'''
Each concern — storage, authentication, paging, request logging — is a small function that
endpoints declare with `Depends`. FastAPI resolves them per request, validates their parameters
and runs the code after `yield` once the response is done. Because endpoints never reach for
globals directly, tests can substitute any dependency through `dependency_overrides`.
''',
"tests": r'''
from fastapi.testclient import TestClient

ADA = {"X-API-Key": "key-ada"}
BOB = {"X-API-Key": "key-bob"}


class TestDependencies(unittest.TestCase):
    def setUp(self):
        self.store = S.NoteStore()
        self.app = S.create_app()
        self.app.dependency_overrides[S.get_store] = lambda: self.store
        self.client = TestClient(self.app)

    def test_store_class(self):
        s = S.NoteStore()
        self.assertEqual(s.add("ada", "x"), {"id": 1, "owner": "ada", "text": "x"})
        s.add("bob", "y")
        self.assertEqual([n["id"] for n in s.for_owner("bob")], [2])

    def test_auth_required(self):
        r = self.client.get("/notes")
        self.assertEqual((r.status_code, r.json()), (401, {"detail": "Invalid API key"}))
        self.assertEqual(r.headers["www-authenticate"], "ApiKey")
        self.assertEqual(self.client.get("/notes", headers={"X-API-Key": "wrong"}).status_code, 401)

    def test_create_and_list_per_user(self):
        r = self.client.post("/notes", json={"text": "hello"}, headers=ADA)
        self.assertEqual((r.status_code, r.json()), (201, {"id": 1, "owner": "ada", "text": "hello"}))
        self.client.post("/notes", json={"text": "bob's"}, headers=BOB)
        self.assertEqual([n["text"] for n in self.client.get("/notes", headers=ADA).json()], ["hello"])
        self.assertEqual(self.client.post("/notes", json={"text": ""}, headers=ADA).status_code, 422)

    def test_pagination(self):
        for i in range(5):
            self.client.post("/notes", json={"text": f"n{i}"}, headers=ADA)
        r = self.client.get("/notes", params={"limit": 2, "offset": 1}, headers=ADA)
        self.assertEqual([n["text"] for n in r.json()], ["n1", "n2"])
        self.assertEqual(self.client.get("/notes", params={"limit": 51}, headers=ADA).status_code, 422)

    def test_override_isolates_global_store(self):
        self.client.post("/notes", json={"text": "kept local"}, headers=ADA)
        self.assertEqual(S.STORE.for_owner("ada"), [])
        self.assertEqual(len(self.store.notes), 1)

    def test_override_user(self):
        self.app.dependency_overrides[S.current_user] = lambda: "tester"
        r = self.client.post("/notes", json={"text": "no key needed"})
        self.assertEqual(r.json()["owner"], "tester")

    def test_yield_cleanup(self):
        S.EVENTS.clear()
        self.client.get("/notes", headers=ADA)
        self.assertEqual(S.EVENTS, ["open", "list", "close"])
''',
"feedback": [
    ("test_auth_required", "Raise HTTPException(401) with the WWW-Authenticate header when the key is missing or unknown."),
    ("test_create_and_list_per_user", "Inject the user and store with Depends; return 201 for creation."),
    ("test_pagination", "Declare the limit/offset constraints in the pagination dependency and slice the notes."),
    ("test_override_isolates_global_store", "Endpoints must get the store through `Depends(get_store)` so tests can override it."),
    ("test_yield_cleanup", "Append 'open', `yield` the list inside try, append 'close' in finally; append 'list' in the endpoint."),
],
},
# ---------------------------------------------------------------- fastapi-async
{
"slug": "fastapi-async", "title": "Async Endpoints and External Services",
"difficulty": "advanced", "prereqs": ["fastapi-dependencies", "asyncio-basics"], "packages": ["fastapi"],
"objectives": ["Write async def endpoints that await an external service",
               "Call several services concurrently with asyncio.gather",
               "Map timeouts and upstream failures to 504 and 502",
               "Test with fake async services injected as dependencies — no network"],
"tags": ["fastapi", "async", "timeouts", "mocking", "concurrency"],
"sources": ["S077", "S061", "S079"], "entry": "class WeatherService; get_weather(); get_settings(); create_app()",
"article": r'''
# Async Endpoints and External Services

## Intuition
Many APIs call *other* APIs: a weather service, a payment provider, a language model. Those calls
mostly wait on the network. With `async def` endpoints, FastAPI's event loop serves other
requests during the wait, and `asyncio.gather` lets one request wait for several services at once
([[asyncio-basics]]). Because the external service is a dependency, tests replace it with a fake
that answers instantly — or never — so every failure path is testable offline.

## Precise explanation
```python
@app.get("/weather/{city}")
async def weather(city: str,
                  service: Annotated[WeatherService, Depends(get_weather)],
                  settings: Annotated[Settings, Depends(get_settings)]):
    try:
        temp = await asyncio.wait_for(service.temperature(city), settings.timeout)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Weather service timed out")
    except LookupError:
        raise HTTPException(404, "Unknown city")
    except Exception:
        raise HTTPException(502, "Weather service error")
    return {"city": city, "temperature": temp}
```
* **def vs async def**: FastAPI runs plain `def` endpoints in a thread pool and `async def`
  endpoints on the event loop. Inside `async def`, never call blocking functions such as
  `time.sleep` or a synchronous HTTP client — they freeze every request.
* **502 Bad Gateway**: the upstream service failed. **504 Gateway Timeout**: it did not answer in
  time. Both are server-side (5xx) because the client did nothing wrong.
* `asyncio.gather(*coros, return_exceptions=True)` returns exceptions as values instead of
  raising the first one, so one failing city does not fail the whole response.
* **Fakes** implement the same async method as the real service. Overriding `get_weather` and
  `get_settings` (a short timeout) makes tests fast and deterministic. A real implementation would
  use an async HTTP client such as `httpx.AsyncClient`.

## Worked example
With a fake returning `{"paris": 18.5}`, `GET /weather/paris` → `{"city": "paris",
"temperature": 18.5}`; a fake that never answers plus a 0.01 s timeout → 504.

## Common mistakes
* `await`ing services one after another in a loop when they could run concurrently.
* Catching `Exception` before `asyncio.TimeoutError`/`LookupError`, so every failure becomes 502.
* Testing against the real service — slow, flaky and possibly paid.

## Why this matters
LLM applications and agents spend most of their time awaiting model and tool calls; the same
timeout, error-mapping and fake-service patterns keep them reliable.
''',
"statement": r'''
Implement:

* `class WeatherService` with `async def temperature(self, city)` that raises
  `RuntimeError("network access is disabled in this course")` (it stands for a real client).
* `class Settings` with attribute `timeout = 1.0`; `get_settings()` returns `Settings()`;
  `get_weather()` returns `WeatherService()`.
* `create_app()` with:
  * `GET /weather/{city}` exactly as in the lesson (504, 404, 502 mapping);
  * `GET /weather` with repeated query parameter `city` (at least one; `Query(min_length=1)`)
    → list, in request order, of `{"city": c, "temperature": t}` or `{"city": c, "error":
    "timeout" | "unknown city" | "service error"}`. Fetch all cities **concurrently** with
    `asyncio.gather(..., return_exceptions=True)`, each wrapped in `asyncio.wait_for` with the
    settings timeout.
''',
"starter": r'''
import asyncio
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query


class WeatherService:
    async def temperature(self, city):
        raise RuntimeError("network access is disabled in this course")


class Settings:
    timeout = 1.0


def get_settings():
    return Settings()


def get_weather():
    return WeatherService()


def create_app():
    app = FastAPI()
    # TODO: GET /weather/{city} and GET /weather
    return app
''',
"hints": [
    "Order the `except` clauses: `asyncio.TimeoutError`, then `LookupError`, then `Exception`.",
    "For the list endpoint: `coros = [asyncio.wait_for(service.temperature(c), settings.timeout) for c in city]` then `await asyncio.gather(*coros, return_exceptions=True)`.",
    "Map each result: `isinstance(r, asyncio.TimeoutError)` → \"timeout\", `isinstance(r, LookupError)` → \"unknown city\", other exceptions → \"service error\".",
],
"solution": r'''
import asyncio
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query


class WeatherService:
    async def temperature(self, city):
        raise RuntimeError("network access is disabled in this course")


class Settings:
    timeout = 1.0


def get_settings():
    return Settings()


def get_weather():
    return WeatherService()


def _describe(city, result):
    if isinstance(result, asyncio.TimeoutError):
        return {"city": city, "error": "timeout"}
    if isinstance(result, LookupError):
        return {"city": city, "error": "unknown city"}
    if isinstance(result, Exception):
        return {"city": city, "error": "service error"}
    return {"city": city, "temperature": result}


def create_app():
    app = FastAPI()

    @app.get("/weather/{city}")
    async def weather(city: str,
                      service: Annotated[WeatherService, Depends(get_weather)],
                      settings: Annotated[Settings, Depends(get_settings)]):
        try:
            temp = await asyncio.wait_for(service.temperature(city), settings.timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Weather service timed out")
        except LookupError:
            raise HTTPException(status_code=404, detail="Unknown city")
        except Exception:
            raise HTTPException(status_code=502, detail="Weather service error")
        return {"city": city, "temperature": temp}

    @app.get("/weather")
    async def weather_many(city: Annotated[list[str], Query(min_length=1)],
                           service: Annotated[WeatherService, Depends(get_weather)],
                           settings: Annotated[Settings, Depends(get_settings)]):
        coros = [asyncio.wait_for(service.temperature(c), settings.timeout) for c in city]
        results = await asyncio.gather(*coros, return_exceptions=True)
        return [_describe(c, r) for c, r in zip(city, results)]

    return app
''',
"explanation": r'''
Both endpoints await the service through `asyncio.wait_for`, so a hung upstream cannot hang the
API. The single-city endpoint maps each failure type to its status code, most specific first. The
multi-city endpoint starts every call at once and uses `return_exceptions=True` so each city's
outcome is reported separately, in request order.
''',
"tests": r'''
import asyncio

from fastapi.testclient import TestClient


class FakeWeather:
    def __init__(self, temps):
        self.temps = temps
        self.active = 0
        self.peak = 0

    async def temperature(self, city):
        self.active += 1
        self.peak = max(self.peak, self.active)
        await asyncio.sleep(0)
        self.active -= 1
        if city == "hang":
            await asyncio.Event().wait()
        if city == "broken":
            raise ConnectionError("upstream down")
        if city not in self.temps:
            raise LookupError(city)
        return self.temps[city]


class FastSettings:
    timeout = 0.05


class TestAsyncEndpoints(unittest.TestCase):
    def setUp(self):
        self.fake = FakeWeather({"paris": 18.5, "oslo": 4.0, "delhi": 31.0})
        self.app = S.create_app()
        self.app.dependency_overrides[S.get_weather] = lambda: self.fake
        self.app.dependency_overrides[S.get_settings] = lambda: FastSettings()
        self.client = TestClient(self.app)

    def test_single_ok(self):
        self.assertEqual(self.client.get("/weather/paris").json(), {"city": "paris", "temperature": 18.5})

    def test_single_errors(self):
        self.assertEqual(self.client.get("/weather/hang").status_code, 504)
        self.assertEqual(self.client.get("/weather/atlantis").status_code, 404)
        r = self.client.get("/weather/broken")
        self.assertEqual((r.status_code, r.json()), (502, {"detail": "Weather service error"}))

    def test_many_in_order(self):
        r = self.client.get("/weather", params=[("city", "oslo"), ("city", "paris"), ("city", "delhi")])
        self.assertEqual(r.json(), [{"city": "oslo", "temperature": 4.0}, {"city": "paris", "temperature": 18.5},
                                    {"city": "delhi", "temperature": 31.0}])

    def test_many_runs_concurrently(self):
        self.client.get("/weather", params=[("city", "oslo"), ("city", "paris"), ("city", "delhi")])
        self.assertEqual(self.fake.peak, 3)

    def test_many_partial_failures(self):
        r = self.client.get("/weather", params=[("city", "paris"), ("city", "hang"), ("city", "x"), ("city", "broken")])
        self.assertEqual(r.json(), [{"city": "paris", "temperature": 18.5}, {"city": "hang", "error": "timeout"},
                                    {"city": "x", "error": "unknown city"}, {"city": "broken", "error": "service error"}])

    def test_requires_city(self):
        self.assertEqual(self.client.get("/weather").status_code, 422)

    def test_real_service_never_used_in_tests(self):
        with self.assertRaises(RuntimeError):
            asyncio.run(S.WeatherService().temperature("paris"))
        self.assertEqual(S.get_settings().timeout, 1.0)
''',
"feedback": [
    ("test_single_errors", "Wrap the call in asyncio.wait_for and catch TimeoutError (504), LookupError (404), then Exception (502)."),
    ("test_many_in_order", "Return one entry per requested city, in request order."),
    ("test_many_runs_concurrently", "Start all calls together with asyncio.gather instead of awaiting them in a loop."),
    ("test_many_partial_failures", "Use `return_exceptions=True` and turn each exception into an error entry."),
    ("test_requires_city", "Declare `city: Annotated[list[str], Query(min_length=1)]`."),
],
},
# ---------------------------------------------------------------- api-testing
{
"slug": "api-testing", "title": "Testing an API",
"difficulty": "advanced", "prereqs": ["fastapi-async", "unit-testing"], "packages": ["fastapi"],
"objectives": ["Write unittest tests for an API with TestClient",
               "Cover success paths, status codes, validation, authentication and missing resources",
               "Keep tests independent by building a fresh app per test",
               "Judge test quality by whether broken versions of the API are caught"],
"tags": ["testing", "api-testing", "testclient", "mutation-testing", "fastapi"],
"sources": ["S078", "S002", "S079"], "entry": "class ApiTests(unittest.TestCase) using self.make_app()",
"article": r'''
# Testing an API

## Intuition
An API is a promise to its clients: these URLs, these status codes, these JSON shapes, these
errors. Tests are how you keep that promise while changing code. In [[unit-testing]] you tested a
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
dependency overrides or fakes ([[fastapi-dependencies]]) instead of real external services.

## Worked example
Creating two notes and reading `GET /notes` should return both, oldest first, with ids 1 and 2 —
one test that catches broken id assignment *and* wrong ordering.

## Common mistakes
* Checking only `status_code == 200` for creation (should be 201).
* Sharing one app across tests, so test order changes results.
* Testing only the happy path, so a missing auth check ships unnoticed.

## Why this matters
These tests are what lets you refactor, upgrade FastAPI or add features without breaking clients.
''',
"statement": r'''
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
''',
"starter": r'''
import unittest
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = ""


def create_app():
    app = FastAPI()
    notes = []

    def check_token(x_token: Annotated[str | None, Header()] = None):
        if x_token != "secret":
            raise HTTPException(status_code=401, detail="Bad token")

    @app.post("/notes", status_code=201, dependencies=[Depends(check_token)])
    def create(note: NoteIn):
        record = {"id": len(notes) + 1, **note.model_dump()}
        notes.append(record)
        return record

    @app.get("/notes/{note_id}")
    def read(note_id: int):
        for n in notes:
            if n["id"] == note_id:
                return n
        raise HTTPException(status_code=404, detail="Note not found")

    @app.get("/notes")
    def list_notes():
        return notes

    return app


TOKEN = {"X-Token": "secret"}


class ApiTests(unittest.TestCase):
    make_app = staticmethod(create_app)

    def setUp(self):
        self.client = TestClient(self.make_app())

    def test_list_starts_empty(self):
        self.assertEqual(self.client.get("/notes").json(), [])

    # TODO: add tests for creation status, token, 404, validation, ids and order
''',
"hints": [
    "One behaviour per test: 201 on create; 401 without the header; 404 for /notes/99; 422 for an empty title.",
    "Create two notes and check the ids are 1 and 2 — that catches the 'every id is 1' bug.",
    "Check that `GET /notes` returns titles in creation order after creating two notes.",
],
"solution": r'''
import unittest
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = ""


def create_app():
    app = FastAPI()
    notes = []

    def check_token(x_token: Annotated[str | None, Header()] = None):
        if x_token != "secret":
            raise HTTPException(status_code=401, detail="Bad token")

    @app.post("/notes", status_code=201, dependencies=[Depends(check_token)])
    def create(note: NoteIn):
        record = {"id": len(notes) + 1, **note.model_dump()}
        notes.append(record)
        return record

    @app.get("/notes/{note_id}")
    def read(note_id: int):
        for n in notes:
            if n["id"] == note_id:
                return n
        raise HTTPException(status_code=404, detail="Note not found")

    @app.get("/notes")
    def list_notes():
        return notes

    return app


TOKEN = {"X-Token": "secret"}


class ApiTests(unittest.TestCase):
    make_app = staticmethod(create_app)

    def setUp(self):
        self.client = TestClient(self.make_app())

    def create(self, title="t", body="b"):
        return self.client.post("/notes", json={"title": title, "body": body}, headers=TOKEN)

    def test_list_starts_empty(self):
        self.assertEqual(self.client.get("/notes").json(), [])

    def test_create_returns_201_and_note(self):
        r = self.create("first", "hello")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json(), {"id": 1, "title": "first", "body": "hello"})

    def test_token_required(self):
        r = self.client.post("/notes", json={"title": "t", "body": "b"})
        self.assertEqual(r.status_code, 401)
        r = self.client.post("/notes", json={"title": "t"}, headers={"X-Token": "wrong"})
        self.assertEqual(r.status_code, 401)

    def test_missing_note_404(self):
        self.assertEqual(self.client.get("/notes/99").status_code, 404)

    def test_empty_title_422(self):
        self.assertEqual(self.create(title="").status_code, 422)

    def test_ids_unique_and_readable(self):
        a, b = self.create("a").json(), self.create("b").json()
        self.assertEqual((a["id"], b["id"]), (1, 2))
        self.assertEqual(self.client.get("/notes/2").json()["title"], "b")

    def test_list_in_creation_order(self):
        self.create("old")
        self.create("new")
        self.assertEqual([n["title"] for n in self.client.get("/notes").json()], ["old", "new"])
''',
"explanation": r'''
Each test targets one promise of the API — status codes, authentication, validation, missing
resources, id assignment and ordering — and builds its own app in `setUp`, so tests are
independent. Because every broken version violates one of those promises, each one fails at
least one test while the correct app passes them all.
''',
"tests": r'''
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field


def build_app(create_status=201, check_token=True, missing_404=True, min_title=1,
              unique_ids=True, newest_first=False):
    class NoteIn(BaseModel):
        title: str = Field(min_length=min_title, max_length=100)
        body: str = ""

    app = FastAPI()
    notes = []

    def token(x_token: Annotated[str | None, Header()] = None):
        if check_token and x_token != "secret":
            raise HTTPException(status_code=401, detail="Bad token")

    @app.post("/notes", status_code=create_status, dependencies=[Depends(token)])
    def create(note: NoteIn):
        record = {"id": len(notes) + 1 if unique_ids else 1, **note.model_dump()}
        notes.append(record)
        return record

    @app.get("/notes/{note_id}")
    def read(note_id: int):
        for n in notes:
            if n["id"] == note_id:
                return n
        if missing_404:
            raise HTTPException(status_code=404, detail="Note not found")
        return None

    @app.get("/notes")
    def list_notes():
        return list(reversed(notes)) if newest_first else notes

    return app


def run_learner_tests(**flags):
    probe = type("Probe", (S.ApiTests,), {"make_app": staticmethod(lambda: build_app(**flags))})
    result = unittest.TestResult()
    unittest.defaultTestLoader.loadTestsFromTestCase(probe).run(result)
    return result


class TestYourApiTests(unittest.TestCase):
    def test_at_least_six_tests(self):
        self.assertGreaterEqual(len(unittest.defaultTestLoader.getTestCaseNames(S.ApiTests)), 6)

    def test_pass_on_correct_app(self):
        result = run_learner_tests()
        self.assertTrue(result.wasSuccessful(), result.failures + result.errors)

    def test_catches_wrong_create_status(self):
        self.assertFalse(run_learner_tests(create_status=200).wasSuccessful())

    def test_catches_missing_token_check(self):
        self.assertFalse(run_learner_tests(check_token=False).wasSuccessful())

    def test_catches_missing_404(self):
        self.assertFalse(run_learner_tests(missing_404=False).wasSuccessful())

    def test_catches_empty_title(self):
        self.assertFalse(run_learner_tests(min_title=0).wasSuccessful())

    def test_catches_duplicate_ids(self):
        self.assertFalse(run_learner_tests(unique_ids=False).wasSuccessful())

    def test_catches_wrong_order(self):
        self.assertFalse(run_learner_tests(newest_first=True).wasSuccessful())
''',
"feedback": [
    ("test_at_least_six_tests", "Add more `test_...` methods to ApiTests."),
    ("test_pass_on_correct_app", "One of your expectations is wrong for the correct app; re-read the API description."),
    ("test_catches_wrong_create_status", "Assert that creating a note returns status 201."),
    ("test_catches_missing_token_check", "Send a request without the X-Token header and expect 401."),
    ("test_catches_missing_404", "Request a note id that does not exist and expect 404."),
    ("test_catches_empty_title", "Post an empty title and expect 422."),
    ("test_catches_duplicate_ids", "Create two notes and check their ids differ (1 and 2)."),
    ("test_catches_wrong_order", "Create two notes and check GET /notes lists them oldest first."),
],
},
]
