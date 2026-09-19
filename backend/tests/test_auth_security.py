import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_create_and_decode_jwt_round_trip(monkeypatch):
    monkeypatch.setenv("ENV", "development")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-for-jwt-auth-1234567890")
    import utils.auth as auth_module
    importlib.reload(auth_module)

    token = auth_module.create_access_token("user@example.com")
    assert auth_module.decode_access_token(token) == "user@example.com"


def test_missing_secret_fails_in_production(monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    import utils.auth as auth_module
    try:
        importlib.reload(auth_module)
    except RuntimeError:
        return

    raise AssertionError("Expected RuntimeError when JWT secret is missing in production")
