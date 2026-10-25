import json


def read_json(headers, body):
    # TODO: 415, 400 or 200
    return 200, json.loads(body)


def validate_item(data):
    errors = []
    # TODO
    return data, errors


def json_response(status, payload):
    # TODO
    return status, {}, json.dumps(payload)
