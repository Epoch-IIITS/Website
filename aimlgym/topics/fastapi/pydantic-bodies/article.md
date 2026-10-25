# Request Bodies with Pydantic

## Learning outcomes

After this lesson you can:

- Describe a JSON body as a Pydantic model with typed, constrained fields
- Forbid unknown fields and choose strict types where coercion would hide errors
- Receive a validated model in a POST endpoint
- Compare Pydantic validation with the hand-written validator

## Intuition
In FA-04 you wrote forty lines to check a name, a price and some tags. **Pydantic**
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
Models are the API's contract: they validate input, shape output (FA-12) and
generate the JSON Schema shown in the docs.

## Library implementation

The test below runs the hand-written rules from FA-04 (extended with `quantity`) and
your Pydantic model over the same payloads and checks that they accept and reject exactly the same
ones. Pydantic also gives you error types, JSON Schema, serialisation and FastAPI integration for
free.

## References

- [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/) — Pydantic (`S080`)
- [FastAPI Tutorial: Request Body](https://fastapi.tiangolo.com/tutorial/body/) — FastAPI (Sebastián Ramírez) (`S073`)
