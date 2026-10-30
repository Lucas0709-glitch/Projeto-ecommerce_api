from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import ALGORITHM, SECRET_KEY
from app.core.security import create_access_token


def test_login_com_sucesso(client, criar_usuario):
    usuario = criar_usuario()

    response = client.post(
        "/auth/login",
        data={"username": usuario["email"], "password": usuario["senha"]},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_com_senha_errada(client, criar_usuario):
    usuario = criar_usuario()

    response = client.post(
        "/auth/login",
        data={"username": usuario["email"], "password": "SenhaErrada999"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"


def test_login_com_email_inexistente(client):
    response = client.post(
        "/auth/login",
        data={"username": "naoexiste@example.com", "password": "qualquer123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"


def test_acesso_sem_token(client):
    response = client.get("/products")

    assert response.status_code == 401


def test_acesso_com_token_invalido(client):
    response = client.get(
        "/products",
        headers={"Authorization": "Bearer token-que-nao-existe"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido ou expirado"


def test_acesso_com_token_expirado(client, criar_usuario):
    usuario = criar_usuario()

    token_expirado = jwt.encode(
        {
            "sub": str(usuario["id"]),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/products",
        headers={"Authorization": f"Bearer {token_expirado}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido ou expirado"


def test_acesso_com_token_de_usuario_inexistente(client):
    token = create_access_token({"sub": "999999"})

    response = client.get(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário não encontrado"


def test_login_ignora_maiusculas_no_email(client, criar_usuario):
    usuario = criar_usuario()

    response = client.post(
        "/auth/login",
        data={
            "username": usuario["email"].upper(),
            "password": usuario["senha"],
        },
    )

    assert response.status_code == 200