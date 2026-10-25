# FA-P2 · Project idea: Notes or Event-RSVP API

**Topic:** FastAPI · ungraded

## Brief

Build a complete small API — either personal notes or event RSVPs for a club — with create, read,
update and delete, validation, an asynchronous call to another service, and a thorough test suite.

## You will use

- FA-10 Request Bodies with Pydantic
- FA-12 Response Models and Status Codes
- FA-13 Dependencies and Dependency Overrides
- FA-14 Async Endpoints and External Services
- FA-15 Testing an API

## Milestones

1. Design the resources and their Pydantic models (input, stored, output).
2. Implement the CRUD endpoints with correct status codes (201, 204, 404, 409).
3. Add filtering and pagination to the list endpoint.
4. Call an external service asynchronously (for example a holiday calendar) and mock it in tests.
5. Reach good test coverage with TestClient, including validation errors.

## Stretch goals

- Add users with hashed passwords and token authentication.
- Persist to SQLite and write migrations.
- Generate a small client from the OpenAPI schema.

## Data

No data is needed; create a few example notes or events in a test fixture.

## Run it yourself

```bash
pip install fastapi uvicorn httpx pytest
uvicorn app:app --reload
```
