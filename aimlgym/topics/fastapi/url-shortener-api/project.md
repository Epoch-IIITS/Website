# FA-P1 · Project idea: URL Shortener API

**Topic:** FastAPI · ungraded

## Brief

Build a URL-shortener service: create short codes for long URLs, redirect visitors, count clicks, and
protect the management endpoints with an API key — with a test suite.

## You will use

- FA-02 HTTP Responses and Status Codes
- FA-03 URLs, Paths and Query Strings
- FA-08 First FastAPI Routes
- FA-10 Request Bodies with Pydantic
- FA-11 Handling Errors in FastAPI
- FA-13 Dependencies and Dependency Overrides

## Milestones

1. POST /links accepts a URL (validated with Pydantic) and returns a short code.
2. GET /{code} redirects with status 307, or returns 404 for unknown codes.
3. Count clicks per code and expose GET /links/{code}/stats.
4. Require an X-API-Key header for creating and deleting links, using a dependency.
5. Write TestClient tests for each endpoint, including errors.

## Stretch goals

- Store links in SQLite instead of a dict.
- Allow custom codes and expiry dates.
- Rate-limit link creation per API key.

## Data

None needed. For persistence, follow FastAPI's [SQL databases tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/).

## Run it yourself

```bash
pip install fastapi uvicorn httpx
uvicorn shortener:app --reload
```
