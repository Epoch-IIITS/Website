# ML-P3 · Project idea: Serve Your Model with FastAPI

**Topic:** Machine Learning · ungraded

## Brief

Put a trained scikit-learn pipeline behind a small web API, so other programs can send a JSON row
and get a prediction back — with input validation, a health check and tests, as a real service
would have.

## You will use

- ML-27 Capstone: an End-to-End Tabular Model
- FA-08 First FastAPI Routes
- FA-10 Request Bodies with Pydantic
- FA-12 Response Models and Status Codes
- FA-15 Testing an API

## Milestones

1. Train and save a pipeline from the capstone or house-price project with joblib.
2. Create a FastAPI app that loads the model once at start-up and exposes GET /health.
3. Add POST /predict with a Pydantic model describing one input row; return the prediction and probability.
4. Reject bad input (missing fields, negative values) with clear 422 errors.
5. Write TestClient tests for a valid request, an invalid one and the health check.

## Stretch goals

- Accept a batch of rows in one request.
- Log each prediction with a timestamp and add GET /stats with simple counts.
- Package the service in a Dockerfile.

## Data

Use the model and data from the capstone (synthetic churn data you generate) or from the
house-price project. See [model persistence](https://scikit-learn.org/stable/model_persistence.html)
for saving pipelines.

## Run it yourself

```bash
pip install fastapi uvicorn scikit-learn joblib pandas httpx
uvicorn app:app --reload
```
Then open http://127.0.0.1:8000/docs to try the endpoints. See
[running a server manually](https://fastapi.tiangolo.com/deployment/manually/).
