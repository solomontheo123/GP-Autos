from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api import auth, orders, payments, vehicles
from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(title="GP Autos API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Paystack-Signature"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret.get_secret_value(),
    session_cookie="gp_oauth_state",
    max_age=600,
    same_site="lax",
    https_only=settings.is_production,
)
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(orders.router)
app.include_router(payments.router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
