from json import JSONDecodeError

from httpx import Response
from pydantic_marshals.contains import TypeChecker, assert_contains


def assert_response(
    response: Response,
    *,
    expected_code: int = 200,
    expected_json: TypeChecker,
    expected_headers: dict[str, TypeChecker] | None = None,
    expected_cookies: dict[str, TypeChecker] | None = None,
) -> Response:
    try:
        json_data = response.json()
    except (UnicodeDecodeError, JSONDecodeError):
        json_data = None

    expected_headers = expected_headers or {}
    if expected_json is not None:
        expected_headers.setdefault("Content-Type", "application/json")
    assert_contains(
        {
            "status_code": response.status_code,
            "headers": response.headers,
            "cookies": response.cookies,
            "json_data": json_data,
        },
        {
            "status_code": expected_code,
            "headers": expected_headers,
            "cookies": expected_cookies or {},
            "json_data": expected_json,
        },
    )
    return response
