import hashlib
import hmac
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return f"pbkdf2_sha256${200000}${salt}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations_raw, salt, digest = password_hash.split("$", 3)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    try:
        iterations = int(iterations_raw)
    except ValueError:
        return False
    computed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return hmac.compare_digest(computed.hex(), digest)


async def find_or_create_google_user(
    session: AsyncSession,
    *,
    google_id: str,
    email: str,
    name: str,
    avatar_url: str | None,
) -> User:
    if session.in_transaction():
        await session.commit()
    async with session.begin():
        user = await session.scalar(
            select(User).where(User.google_id == google_id).with_for_update()
        )
        if user is None:
            user = await session.scalar(select(User).where(User.email == email).with_for_update())
        if user is None:
            user = User(google_id=google_id, email=email, name=name, avatar_url=avatar_url)
            session.add(user)
        else:
            user.google_id = google_id
            user.email = email
            user.name = name
            user.avatar_url = avatar_url
        await session.flush()
    return user
