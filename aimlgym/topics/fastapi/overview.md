# FastAPI

**You will be able to:** Understand HTTP messages, URLs, JSON and routing by hand, then build, validate, secure, run asynchronously and test FastAPI services.

**Topic prerequisites:** Python

Web APIs from first principles. The first half uses only the standard library: the structure
of HTTP requests and responses, status codes, URLs and query strings, JSON bodies, a hand-made
router, `asyncio`, and a minimal ASGI application. The second half rebuilds the same ideas with
FastAPI — routes, typed parameters and validation, Pydantic request bodies, error handling,
response models, dependencies, asynchronous endpoints — and finishes by writing API tests.

**Packages:** standard library for steps 1–7; `fastapi` (with `httpx`, used by
`fastapi.testclient.TestClient`) from step 8. No server is started and no network is used:
tests call the application in-process, and external services are replaced by fakes.
**Prerequisite:** the Python topic only; you can take this topic any time after Python.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | FA-01 | [Anatomy of an HTTP Request](http-requests/problem.md) | beginner | PY-23 |
| 2 | FA-02 | [HTTP Responses and Status Codes](http-responses/problem.md) | beginner | FA-01 |
| 3 | FA-03 | [URLs, Paths and Query Strings](urls-query/problem.md) | beginner | FA-02 |
| 4 | FA-04 | [JSON Request Bodies and Validation](json-bodies/problem.md) | intermediate | FA-03 |
| 5 | FA-05 | [A Router by Hand](manual-router/problem.md) | intermediate | FA-04 |
| 6 | FA-06 | [async and await with asyncio](asyncio-basics/problem.md) | intermediate | FA-05 |
| 7 | FA-07 | [A Minimal ASGI Application](asgi-app/problem.md) | intermediate | FA-06 |
| 8 | FA-08 | [First FastAPI Routes](fastapi-routes/problem.md) | intermediate | FA-07 |
| 9 | FA-09 | [Query and Path Parameters with Validation](fastapi-params/problem.md) | intermediate | FA-08 |
| 10 | FA-10 | [Request Bodies with Pydantic](pydantic-bodies/problem.md) | intermediate | FA-09, FA-04 |
| 11 | FA-11 | [Handling Errors in FastAPI](fastapi-errors/problem.md) | intermediate | FA-10 |
| 12 | FA-12 | [Response Models and Status Codes](response-models/problem.md) | advanced | FA-11 |
| 13 | FA-13 | [Dependencies and Dependency Overrides](fastapi-dependencies/problem.md) | advanced | FA-12 |
| 14 | FA-P1 | [Project idea: URL Shortener API](url-shortener-api/project.md) | ungraded | FA-02, FA-03, FA-08, FA-10, FA-11, FA-13 |
| 15 | FA-14 | [Async Endpoints and External Services](fastapi-async/problem.md) | advanced | FA-13, FA-06 |
| 16 | FA-15 | [Testing an API](api-testing/problem.md) | advanced | FA-14, PY-27 |
| 17 | FA-P2 | [Project idea: Notes or Event-RSVP API](notes-rsvp-api/project.md) | ungraded | FA-10, FA-12, FA-13, FA-14, FA-15 |
