"""Ungraded project ideas for the FastAPI topic (library revision, Phase 6)."""

PROBLEMS = [
{
"kind": "project", "slug": "url-shortener-api", "title": "URL Shortener API",
"tags": ["web-api", "fastapi", "authentication"],
"brief": r'''
Build a URL-shortener service: create short codes for long URLs, redirect visitors, count clicks, and
protect the management endpoints with an API key — with a test suite.
''',
"uses": ["http-responses", "urls-query", "fastapi-routes", "pydantic-bodies", "fastapi-errors", "fastapi-dependencies"],
"milestones": [
    "POST /links accepts a URL (validated with Pydantic) and returns a short code.",
    "GET /{code} redirects with status 307, or returns 404 for unknown codes.",
    "Count clicks per code and expose GET /links/{code}/stats.",
    "Require an X-API-Key header for creating and deleting links, using a dependency.",
    "Write TestClient tests for each endpoint, including errors.",
],
"stretch": [
    "Store links in SQLite instead of a dict.",
    "Allow custom codes and expiry dates.",
    "Rate-limit link creation per API key.",
],
"data": r'''
None needed. For persistence, follow FastAPI's [SQL databases tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/).
''',
"setup": r'''
```bash
pip install fastapi uvicorn httpx
uvicorn shortener:app --reload
```
''',
},
{
"kind": "project", "slug": "notes-rsvp-api", "title": "Notes or Event-RSVP API",
"tags": ["web-api", "fastapi", "crud"],
"brief": r'''
Build a complete small API — either personal notes or event RSVPs for a club — with create, read,
update and delete, validation, an asynchronous call to another service, and a thorough test suite.
''',
"uses": ["pydantic-bodies", "response-models", "fastapi-dependencies", "fastapi-async", "api-testing"],
"milestones": [
    "Design the resources and their Pydantic models (input, stored, output).",
    "Implement the CRUD endpoints with correct status codes (201, 204, 404, 409).",
    "Add filtering and pagination to the list endpoint.",
    "Call an external service asynchronously (for example a holiday calendar) and mock it in tests.",
    "Reach good test coverage with TestClient, including validation errors.",
],
"stretch": [
    "Add users with hashed passwords and token authentication.",
    "Persist to SQLite and write migrations.",
    "Generate a small client from the OpenAPI schema.",
],
"data": r'''
No data is needed; create a few example notes or events in a test fixture.
''',
"setup": r'''
```bash
pip install fastapi uvicorn httpx pytest
uvicorn app:app --reload
```
''',
},
]
