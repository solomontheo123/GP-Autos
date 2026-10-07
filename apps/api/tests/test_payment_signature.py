import hashlib
import hmac

from app.core.config import Settings
from app.services.payment_service import verify_webhook_signature


def test_paystack_signature_matches_sha512_hmac(monkeypatch) -> None:
    secret = "sk_test_local"
    body = b'{"event":"charge.success"}'
    monkeypatch.setattr(
        "app.services.payment_service.settings.paystack_secret_key.get_secret_value", lambda: secret
    )
    signature = hmac.new(secret.encode(), body, hashlib.sha512).hexdigest()

    assert verify_webhook_signature(body, signature)
    assert not verify_webhook_signature(body, "invalid")
    assert not verify_webhook_signature(body, None)


def test_paystack_callback_defaults_to_frontend_confirmation_route() -> None:
    settings = Settings(frontend_url="https://gp-autos.vercel.app", paystack_callback_url="")

    assert settings.paystack_callback_url == "https://gp-autos.vercel.app/orders/confirmation"


def test_paystack_callback_defaults_to_production_frontend_in_production_env() -> None:
    settings = Settings(environment="production", frontend_url="", paystack_callback_url="")

    assert settings.paystack_callback_url == "https://gp-autos.vercel.app/orders/confirmation"
