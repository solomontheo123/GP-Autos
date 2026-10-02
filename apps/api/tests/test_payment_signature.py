import hashlib
import hmac

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
