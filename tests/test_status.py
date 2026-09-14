from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_home():
    response = cliente.get("/")

    assert response.status_code == 200
    assert "API Status Checker" in response.text
    assert "Ver Status" in response.text


def test_status():
    response = cliente.get("/status")

    assert response.status_code == 200
    assert "Status: OK" in response.text
    assert "Tudo funcionando!" in response.text


