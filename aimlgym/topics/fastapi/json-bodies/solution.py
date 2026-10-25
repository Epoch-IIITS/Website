r"""Reference solution for FA-04 JSON Request Bodies and Validation.

The three checks run from the cheapest and most general (media type) to the most specific (field
rules), each with its own status code. Validation collects every error with a location instead of
stopping at the first, rejects booleans explicitly, and returns a cleaned copy rather than the
caller's dict.
"""
import json

FIELDS = {"name", "price", "tags"}


def read_json(headers, body):
    media = headers.get("content-type", "").split(";")[0].strip().lower()
    if media != "application/json":
        return 415, {"detail": "Content-Type must be application/json"}
    try:
        return 200, json.loads(body)
    except json.JSONDecodeError:
        return 400, {"detail": "Invalid JSON"}


def _err(field, msg):
    return {"loc": ["body", field], "msg": msg}


def validate_item(data):
    if not isinstance(data, dict):
        return None, [{"loc": ["body"], "msg": "must be an object"}]
    errors = []
    name = data.get("name")
    if "name" not in data:
        errors.append(_err("name", "field required"))
    elif not isinstance(name, str) or not name.strip():
        errors.append(_err("name", "must be a non-empty string"))
    price = data.get("price")
    if "price" not in data:
        errors.append(_err("price", "field required"))
    elif not isinstance(price, (int, float)) or isinstance(price, bool):
        errors.append(_err("price", "must be a number"))
    elif price < 0:
        errors.append(_err("price", "must be >= 0"))
    tags = data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        errors.append(_err("tags", "must be a list of strings"))
    for extra in sorted(set(data) - FIELDS):
        errors.append(_err(extra, "extra field not allowed"))
    if errors:
        return None, errors
    return {"name": name.strip(), "price": price, "tags": list(tags)}, []


def json_response(status, payload):
    return status, {"content-type": "application/json"}, json.dumps(payload, separators=(",", ":"))
