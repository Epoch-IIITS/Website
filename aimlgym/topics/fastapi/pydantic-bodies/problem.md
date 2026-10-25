# FA-10 · Request Bodies with Pydantic

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** fastapi

**Builds on:** FA-09 Query and Path Parameters with Validation, FA-04 JSON Request Bodies and Validation

Read the lesson first: [article.md](article.md)

## Task

1. Define `class Item(BaseModel)` exactly as in the lesson (fields `name`, `price`, `tags`,
   `quantity`, with `extra="forbid"` and `str_strip_whitespace=True`).
2. `parse_item(data)` → `Item.model_validate(data)` (let `ValidationError` propagate).
3. `app = FastAPI()` with `POST /items` returning
   `{"item": item.model_dump(), "total": item.price * item.quantity}`.

## Hints

<details><summary>Hint 1</summary>

`model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)` goes in the class body.

</details>

<details><summary>Hint 2</summary>

`price: float = Field(ge=0, strict=True)` and `quantity: int = Field(default=0, ge=0, strict=True)`.

</details>

<details><summary>Hint 3</summary>

`@app.post("/items")` above `def create_item(item: Item):`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_parse_and_defaults` | Strip whitespace via model_config and give tags and quantity defaults. |
| `test_errors_listed` | Use `extra="forbid"`, `min_length=1` on name and a strict float price. |
| `test_strict_types` | Strict numbers reject booleans and floats for ints; list[str] checks every tag; limit name to 50 characters. |
| `test_post_ok` | The endpoint takes `item: Item` and returns the dumped model and price * quantity. |
| `test_post_422` | FastAPI reports body errors with loc ['body', field] when the model is the only body parameter. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The model states every rule declaratively; strict numeric fields and `extra="forbid"` reproduce
the hand-written validator's behaviour, and whitespace stripping happens before the length check.
FastAPI validates the body against the model and passes a typed object to the endpoint.

## References

- [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/) — Pydantic (`S080`)
- [FastAPI Tutorial: Request Body](https://fastapi.tiangolo.com/tutorial/body/) — FastAPI (Sebastián Ramírez) (`S073`)
