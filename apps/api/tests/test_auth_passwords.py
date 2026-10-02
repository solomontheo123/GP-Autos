from app.services.auth_service import hash_password, verify_password


def test_hash_and_verify_password_round_trip() -> None:
    raw_password = "SecurePass!2026"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("wrong-password", hashed) is False
