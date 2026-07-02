from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, status

from app.api.dependencies import CurrentUserDep, SessionDep
from app.schemas.auth import AuthStatusResponse, UserCreate, UserLogin, UserPublic
from app.services.auth_service import DuplicateEmailError, InvalidCredentialsError, auth_service
from app.settings import settings

router = APIRouter()


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path="/",
    )


def _clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.cookie_name, path="/")


@router.post("/register", response_model=AuthStatusResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, response: Response, session: SessionDep) -> AuthStatusResponse:
    try:
        user = auth_service.register_user(session, payload)
    except DuplicateEmailError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"code": "EMAIL_ALREADY_EXISTS", "message": str(exc), "details": None}) from exc

    token = auth_service.issue_token(str(user.id))
    _set_auth_cookie(response, token)
    return AuthStatusResponse(user=UserPublic.model_validate(user), authenticated=True)


@router.post("/login", response_model=AuthStatusResponse)
def login(payload: UserLogin, response: Response, session: SessionDep) -> AuthStatusResponse:
    try:
        user = auth_service.authenticate_user(session, payload)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "INVALID_CREDENTIALS", "message": str(exc), "details": None}) from exc

    token = auth_service.issue_token(str(user.id))
    _set_auth_cookie(response, token)
    return AuthStatusResponse(user=UserPublic.model_validate(user), authenticated=True)


@router.post("/logout", response_model=dict[str, str])
def logout(response: Response) -> dict[str, str]:
    _clear_auth_cookie(response)
    return {"message": "Logged out"}


@router.get("/me", response_model=AuthStatusResponse)
def me(user: CurrentUserDep) -> AuthStatusResponse:
    return AuthStatusResponse(user=UserPublic.model_validate(user), authenticated=True)
