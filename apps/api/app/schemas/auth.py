from uuid import UUID

from pydantic import BaseModel


class AuthUserRead(BaseModel):
    id: UUID
    email: str
    name: str
    avatar_url: str | None
