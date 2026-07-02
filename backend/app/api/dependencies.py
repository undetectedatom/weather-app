from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, status
from sqlmodel import Session

from app.database.engine import get_session
from app.database.models import User
from app.services.auth_service import auth_service
from app.settings import settings

SessionDep = Annotated[Session, Depends(get_session)]


def get_cur_user(
    session: SessionDep,
    auth_cookie: Annotated[str | None, Cookie(alias=settings.cookie_name)] = None,
) -> User:
    if not auth_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_REQUIRED", "message": "Authentication is required", "details": None},
        )

    try:
        user_id = auth_service.verify_token(auth_cookie)
        parsed_user_id = UUID(user_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_REQUIRED", "message": "Invalid authentication token", "details": None},
        ) from exc

    user = session.get(User, parsed_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_REQUIRED", "message": "Authenticated user no longer exists", "details": None},
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_cur_user)]
