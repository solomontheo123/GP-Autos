from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


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
