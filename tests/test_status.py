from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)

def test_status():
    response = cliente.get("/status") ## GET no PAth

    assert response.status_code == 200 # Valida resposta em /status 
    assert response.json() == {"status": "ok"} # Valida o conteúdo do Endpoint
