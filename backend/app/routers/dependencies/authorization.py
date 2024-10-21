from datetime import timedelta
from typing import Annotated, Final

from fastapi import Depends, HTTPException, Response
from fastapi.security import APIKeyCookie

from app.common.utils import datetime_utc_now
from app.models.participants_db import Participant

auth_cookie_name: Final[str] = "scan_quest_auth_token"
cookie_auth_scheme = APIKeyCookie(
    name=auth_cookie_name, auto_error=False, scheme_name="auth cookie"
)


class AuthCookieSetterDep:
    def __init__(self, response: Response) -> None:
        self.response = response

    def __call__(self, auth_token: str) -> None:
        self.response.set_cookie(
            key=auth_cookie_name,
            value=auth_token,
            expires=datetime_utc_now() + timedelta(days=1),
            secure=True,
            httponly=True,
            samesite="strict",
        )


AuthCookieSetter = Annotated[AuthCookieSetterDep, Depends(AuthCookieSetterDep)]


missing_cookie_exception = HTTPException(
    status_code=401, detail="Auth cookie is missing"
)
invalid_cookie_exception = HTTPException(
    status_code=401, detail="Auth cookie is invalid"
)


async def load_participant_by_cookie(
    auth_token: Annotated[str | None, Depends(cookie_auth_scheme)] = None
) -> Participant:
    if auth_token is None:
        raise missing_cookie_exception

    participant = await Participant.find_first_by_kwargs(auth_token=auth_token)
    if participant is None:
        raise invalid_cookie_exception
    return participant


ParticipantByCookie = Annotated[Participant, Depends(load_participant_by_cookie)]
