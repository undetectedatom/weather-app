from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os

from sqlmodel import Session, select

from app.database.models import User
from app.schemas.auth import UserCreate, UserLogin
from app.settings import settings


class DuplicateEmailError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def register_user(self, session: Session, payload: UserCreate) -> User:
        existing = session.exec(select(User).where(User.email == payload.email)).first()
        if existing:
            raise DuplicateEmailError("An account with this email already exists")

        user = User(email=payload.email, password_hash=self.hash_password(payload.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def authenticate_user(self, session: Session, payload: UserLogin) -> User:
        user = session.exec(select(User).where(User.email == payload.email)).first()
        if not user or not self.verify_password(payload.password, user.password_hash):
            raise InvalidCredentialsError("Email or password is incorrect")
        return user

    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return f"{base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        salt_b64, digest_b64 = password_hash.split("$", 1)
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(digest_b64.encode())
        digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(digest, expected)

    def issue_token(self, user_id: str) -> str:
        payload = base64.urlsafe_b64encode(json.dumps({"sub": user_id}, separators=(",", ":")).encode()).decode()
        signature = hmac.new(self.secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return f"{payload}.{signature}"

    def verify_token(self, token: str) -> str:
        try:
            payload, signature = token.split(".", 1)
        except ValueError as exc:
            raise InvalidCredentialsError("Invalid auth token") from exc
        expected = hmac.new(self.secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise InvalidCredentialsError("Invalid auth token")
        data = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
        if "sub" not in data:
            raise InvalidCredentialsError("Invalid auth token")
        return str(data["sub"])


auth_service = AuthService(secret=settings.cookie_secret)
