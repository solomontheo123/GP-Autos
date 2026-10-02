from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.core.oauth import oauth
from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import AuthUserRead
from app.services.auth_service import find_or_create_google_user

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
        samesite="lax",
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
