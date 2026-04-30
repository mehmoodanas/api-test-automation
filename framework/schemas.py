"""
JSON schemas describing the expected shape of API responses.

Used with the `jsonschema` library to assert that responses match
their contract — catches missing fields, wrong types, or unexpected
changes in the API.
"""

# JSONPlaceholder /posts
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

# Restful Booker /auth response
AUTH_TOKEN_SCHEMA = {
    "type": "object",
    "required": ["token"],
    "properties": {
        "token": {"type": "string", "minLength": 8},
    },
}

# Restful Booker /booking model
BOOKING_SCHEMA = {
    "type": "object",
    "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
        },
        "additionalneeds": {"type": "string"},
    },
}

# Restful Booker /booking POST response wraps the booking
CREATE_BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA,
    },
}
