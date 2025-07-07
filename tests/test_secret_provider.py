from src.infra.secret_provider import get_secret
import pytest


def test_get_secret_valid(monkeypatch):
    monkeypatch.setenv("SOME_KEY", "val")
    assert get_secret("SOME_KEY") == "val"


def test_get_secret_missing(monkeypatch):
    monkeypatch.delenv("NO_KEY", raising=False)
    with pytest.raises(KeyError):
        get_secret("NO_KEY")
