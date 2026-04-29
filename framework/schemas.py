"""
JSON schemas describing the expected shape of API responses.

Used with the `jsonschema` library to assert that responses match
their contract — catches missing fields, wrong types, or unexpected
changes in the API.
"""

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "additionalProperties": False,
}