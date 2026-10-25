r"""Reference solution for AG-15 Validate-and-Retry Tool Calls.

Validation checks each field in a fixed order and stops at its first problem, producing precise,
stable messages. The retry loop gives the model its previous output plus those messages, stops at the
first valid result, and records every failed attempt's errors for debugging.
"""
import json


def _type_ok(v, t):
    if t in (int, float) and isinstance(v, bool):
        return False
    if t is float:
        return isinstance(v, (int, float))
    return isinstance(v, t)


def validate(obj, schema):
    if not isinstance(obj, dict):
        return ["expected a JSON object"]
    errors = []
    for f in sorted(schema):
        spec = schema[f]
        if f not in obj:
            if spec.get("required", True):
                errors.append(f"{f}: missing")
            continue
        v = obj[f]
        if not _type_ok(v, spec["type"]):
            errors.append(f"{f}: expected {spec['type'].__name__}")
            continue
        if "enum" in spec and v not in spec["enum"]:
            errors.append(f"{f}: must be one of {spec['enum']!r}")
            continue
        if "min" in spec and v < spec["min"]:
            errors.append(f"{f}: must be >= {spec['min']}")
            continue
        if "max" in spec and v > spec["max"]:
            errors.append(f"{f}: must be <= {spec['max']}")
    for f in sorted(set(obj) - set(schema)):
        errors.append(f"{f}: unexpected field")
    return errors


def call_with_retries(model, prompt, schema, max_attempts=3):
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    messages = [prompt]
    all_errors = []
    for attempt in range(1, max_attempts + 1):
        text = model(list(messages))
        try:
            obj = json.loads(text)
            errors = validate(obj, schema)
        except json.JSONDecodeError:
            obj, errors = None, ["invalid JSON"]
        if not errors:
            return {"ok": True, "value": obj, "attempts": attempt, "errors": all_errors}
        all_errors.append(errors)
        messages.append(text)
        messages.append("Your output was invalid: " + "; ".join(errors))
    return {"ok": False, "value": None, "attempts": max_attempts, "errors": all_errors}
