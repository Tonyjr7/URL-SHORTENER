import os
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

# Ensure project root is on sys.path so "routes" package can be imported
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from routes.shorten import router as shorten_router

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(shorten_router)
    return app

def test_shorten_success(monkeypatch, app):
    # Arrange: valid URL, deterministic code, capture add_url call
    called = {}
    monkeypatch.setattr(shorten_router, "is_valid_url", lambda url: True)
    monkeypatch.setattr(shorten_router, "generate_code", lambda: "abc123")
    def fake_add_url(original_url, short_code):
        called["url"] = original_url
        called["code"] = short_code
    monkeypatch.setattr(shorten_router, "add_url", fake_add_url)

    client = TestClient(app)

    # Act
    resp = client.post("/shorten", json={"original_url": "https://example.com"})

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert body["status_code"] == 200
    assert body["message"] == "URL shortened successfully"
    assert body["data"]["short_link"] == "abc123"
    assert called["url"] == "https://example.com"
    assert called["code"] == "abc123"

def test_shorten_invalid_url(monkeypatch, app):
    monkeypatch.setattr(shorten_router, "is_valid_url", lambda url: False)
    client = TestClient(app)

    resp = client.post("/shorten", json={"original_url": "not-a-url"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["status_code"] == 400
    assert "Invalid URL" in body["message"]

def test_shorten_db_error(monkeypatch, app):
    monkeypatch.setattr(shorten_router, "is_valid_url", lambda url: True)
    monkeypatch.setattr(shorten_router, "generate_code", lambda: "abc123")
    def raise_err(original_url, short_code):
        raise Exception("db failed")
    monkeypatch.setattr(shorten_router, "add_url", raise_err)

    client = TestClient(app)
    resp = client.post("/shorten", json={"original_url": "https://example.com"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["status_code"] == 500
    assert "db failed" in body["data"]["error"]