from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.core.oauth import oauth
from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import AuthUserRead, EmailLoginRequest, EmailRegisterRequest
from app.services.auth_service import (
    find_or_create_google_user,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["authentication"])


def _session_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        settings.session_secret.get_secret_value(), salt="gp-autos-session"
    )


def _set_session(response: Response, user: User) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=_session_serializer().dumps(str(user.id)),
        max_age=settings.session_max_age_seconds,
        httponly=True,
        secure=settings.is_production,
        samesite="none" if settings.is_production else "lax",
        path="/",
    )


@router.get("/google")
async def google_login(request: Request) -> RedirectResponse:
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google OAuth is not configured"
        )
    callback_uri = settings.google_redirect_uri
    return cast(RedirectResponse, await oauth.google.authorize_redirect(request, callback_uri))


@router.get("/google/callback")
async def google_callback(
    request: Request, session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Google sign-in failed"
        ) from None
    profile = token.get("userinfo")
    if not isinstance(profile, dict) or not profile.get("sub") or not profile.get("email"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Google profile is incomplete"
        )
    if profile.get("email_verified") is not True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Google email is not verified"
        )
    user = await find_or_create_google_user(
        session,
        google_id=str(profile["sub"]),
        email=str(profile["email"]),
        name=str(profile.get("name") or profile["email"]),
        avatar_url=str(profile["picture"]) if profile.get("picture") else None,
    )
    await session.commit()
    response = RedirectResponse(url=settings.frontend_url, status_code=status.HTTP_303_SEE_OTHER)
    _set_session(response, user)
    return response


@router.post("/register", response_model=AuthUserRead)
async def register_user(
    payload: EmailRegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> AuthUserRead:
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match.",
        )

    normalized_email = payload.email.lower().strip()
    existing_user = await session.scalar(select(User).where(User.email == normalized_email))
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user = User(
        email=normalized_email,
        name=payload.name.strip(),
        password_hash=hash_password(payload.password),
        google_id=None,
        avatar_url=None,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    response.status_code = status.HTTP_201_CREATED
    _set_session(response, user)
    return AuthUserRead(id=user.id, email=user.email, name=user.name, avatar_url=user.avatar_url)


@router.post("/login", response_model=AuthUserRead)
async def login_user(
    payload: EmailLoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> AuthUserRead:
    normalized_email = payload.email.lower().strip()
    user = await session.scalar(select(User).where(User.email == normalized_email))
    if user is None or user.password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    _set_session(response, user)
    return AuthUserRead(id=user.id, email=user.email, name=user.name, avatar_url=user.avatar_url)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout() -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(
        settings.session_cookie_name,
        path="/",
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
    )
    return response


@router.get("/me", response_model=AuthUserRead)
async def current_user(user: User = Depends(get_current_user)) -> AuthUserRead:
    return AuthUserRead(id=user.id, email=user.email, name=user.name, avatar_url=user.avatar_url)
