# GP Autos

GP Autos is an automotive marketplace foundation for discovering and purchasing vehicles in Nigeria. This release implements the HNG 15 Lesson 2 individual shop flow as a real vehicle-listing, checkout, order, payment, and confirmation-email slice. It does not implement the HNG team task.

## Architecture

- `apps/web`: Next.js 16 App Router storefront, TypeScript, React 19, Tailwind CSS 4.
- `apps/api`: FastAPI API, Pydantic, SQLAlchemy 2.1 async, Alembic, psycopg 3, and uv.
- PostgreSQL is the source of truth. Neon is the target hosted provider.
- Google OAuth authenticates users through a server-side authorization-code flow and signed HTTP-only session cookie.
- Paystack initialization, transaction verification, webhook signature validation, and order state changes run on the API.
- Mailgun sends confirmation email only after successful server-side payment verification.

## Features

- Vehicle discovery, listing details, six Nigerian-market seed listings, and responsive marketplace UI.
- Persistent browser cart containing only listing IDs and quantities.
- Server-side availability, inventory reservation, and price calculation during order creation.
- User-scoped order history and detail APIs/pages.
- Paystack initialization and verification by reference, plus idempotent signed webhook handling.
- Mailgun HTML and plain-text confirmation message with send-once state.

## Project Structure

```text
apps/
  web/                 Next.js storefront
  api/                 FastAPI service and Alembic migrations
    app/api/           REST endpoints
    app/models/        SQLAlchemy entities
    app/services/      business logic and provider integrations
    alembic/           database migration history
    tests/             API logic tests
```

## Local Setup

Requirements: Node.js 20.9+, Python 3.14, and uv 0.12.21 or newer.

1. Install the frontend dependencies: `cd apps/web && npm install`.
2. Copy the root `.env.example` to `apps/web/.env.local`.
3. Copy `apps/api/.env.example` to `apps/api/.env` and set `DATABASE_URL`.
4. From `apps/api`, run `uv sync`.
5. Apply migrations with `uv run alembic upgrade head`.
6. Seed development vehicles with `uv run python -m app.seed`.
7. Run the API with `uv run uvicorn app.main:app --reload --port 8000` from `apps/api`.
8. Run the storefront with `npm run dev` from `apps/web`.

Alternatively, root scripts include `npm run dev:web`, `npm run dev:api`, `npm run test:api`, `npm run check:api`, `npm run lint:web`, `npm run typecheck:web`, and `npm run build:web`.

## Environment Variables

Frontend (`apps/web/.env.local`):

- `NEXT_PUBLIC_API_URL`: API origin, normally `http://localhost:8000`.

Backend (`apps/api/.env`):

- `DATABASE_URL`: Neon PostgreSQL connection string using `postgresql+psycopg://` and Neon SSL settings.
- `FRONTEND_URL`: allowed browser origin; local default `http://localhost:3000`.
- `SESSION_SECRET`: random secret of at least 32 bytes.
- `ENVIRONMENT`: `development` or `production`.
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`.
- `PAYSTACK_SECRET_KEY`, `PAYSTACK_PUBLIC_KEY`, `PAYSTACK_CALLBACK_URL`.
- `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, `MAILGUN_FROM_EMAIL`, `MAILGUN_BASE_URL`.

Never place backend secrets in a `NEXT_PUBLIC_` variable.

## Neon Setup

Create a Neon PostgreSQL project, copy the pooled or direct connection string, and set `DATABASE_URL` in `apps/api/.env`. The driver URL must use `postgresql+psycopg://`. Run `uv run alembic upgrade head` from `apps/api`. The repository includes an initial migration for users, vehicle listings, orders, order items, state enums, indexes, and constraints.

## Google OAuth Setup

In Google Cloud Console, create an OAuth 2.0 Web application client, configure the consent screen, and add the exact authorized redirect URI:

- Local: `http://localhost:8000/auth/google/callback`
- Production: `https://<backend-domain>/auth/google/callback`

Set the returned client ID/secret and the exact matching URI as `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REDIRECT_URI`. Google OAuth has not been exercised against a real Cloud Console client in this workspace.

## Paystack Setup

Use Paystack test keys while developing. Store the secret and public keys only in backend environment configuration. Set:

- `PAYSTACK_SECRET_KEY`: test or live secret key.
- `PAYSTACK_PUBLIC_KEY`: corresponding public key, not used for secret operations.
- `PAYSTACK_CALLBACK_URL`: local `http://localhost:3000/orders/confirmation`; production `https://<frontend-domain>/orders/confirmation`.

Configure the Paystack webhook endpoint as `https://<backend-domain>/api/payments/webhook`. The endpoint validates `x-paystack-signature`, then independently verifies successful transactions with Paystack before changing order state. A live/test transaction was not possible without credentials.

## Mailgun Setup

Create a Mailgun sending domain and API key, verify sender/domain DNS records, then set `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, `MAILGUN_FROM_EMAIL`, and `MAILGUN_BASE_URL`. The service uses Mailgun's HTTP API; no Mailgun credential was available for sending a real message.

## Database Migrations and Seed Data

- Apply migrations: `cd apps/api && uv run alembic upgrade head`.
- Create a new migration after model changes: `uv run alembic revision --autogenerate -m "describe change"`.
- Seed or refresh six development vehicles: `uv run python -m app.seed`.
- Migration SQL can be reviewed without a database using `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/gp_autos uv run alembic upgrade head --sql`.

## Testing

- Frontend: `npm run lint`, `npm run typecheck`, and `npm run build` in `apps/web`.
- Backend: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy app` in `apps/api`.
- Current tests cover order input constraints and Paystack webhook HMAC verification. End-to-end database/provider tests require a running PostgreSQL database and provider credentials.

## Deployment

Deploy `apps/web` as a Next.js application and `apps/api` as an ASGI service. Set `NEXT_PUBLIC_API_URL` to the deployed API origin, `FRONTEND_URL` to the deployed frontend origin, and configure credentialed CORS for that exact origin. Apply Alembic migrations during deployment. Register the production Google redirect URI and Paystack callback/webhook URLs exactly as documented above. Use production Google, Paystack, and Mailgun credentials only in the backend secret manager, and set `ENVIRONMENT=production` so session cookies are `Secure`.

## Delivery Status

- Implemented: marketplace pages, local cart, FastAPI routes, SQLAlchemy models, initial Alembic migration, seed data, OAuth/session, Paystack service and webhook, Mailgun service, and order pages.
- Tested: frontend lint/typecheck/build; backend Ruff, MyPy, Pytest; offline PostgreSQL migration SQL generation.
- Requires credentials: Neon, Google OAuth, Paystack, and Mailgun are implemented but not externally configured or exercised.
- Requires production configuration: service deployment, production origins, provider dashboard values, webhook registration, and migration application to the target database.
