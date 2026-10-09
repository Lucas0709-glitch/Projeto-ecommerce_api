from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rota_principal():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "E-commerce API funcionando!"
    }

def test_cadastrar_usuario():
    response = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": "teste_automatizado_190@example.com",
            "senha": "senha_teste_123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Usuario Teste"
    assert data["email"] == "teste_automatizado@example.com"
    assert "id" in data
    assert "senha" not in data
    assert "senha_hash" not in data

def test_impedir_email_duplicado():
    email = "email_duplicado@example.com"

    primeiro_usuario = client.post(
        "/users",
        json={
            "nome": "Primeiro Usuario",
            "email": email,
            "senha": "senha_teste_123"
        }
    )

    assert primeiro_usuario.status_code == 201

    segundo_usuario = client.post(
        "/users",
        json={
            "nome": "Segundo Usuario",
            "email": email,
            "senha": "outra_senha_123"
        }
    )

    assert segundo_usuario.status_code == 400
    assert segundo_usuario.json()["detail"] == "E-mail já cadastrado"