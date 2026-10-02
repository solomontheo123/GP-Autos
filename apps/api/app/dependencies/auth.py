from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_session
from app.models.user import User


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        settings.session_secret.get_secret_value(), salt="gp-autos-session"
    )


async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    session_cookie = request.cookies.get(settings.session_cookie_name)
    if not session_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    try:
        user_id = UUID(
            _serializer().loads(session_cookie, max_age=settings.session_max_age_seconds)
        )
    except BadSignature, SignatureExpired, ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired"
        ) from None
    user = await session.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session user not found"
        )
    return user
