from uuid import uuid4


def test_cadastrar_usuario(client):
    email = f"cadastro_{uuid4().hex}@example.com"

    response = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": email,
            "senha": "senha_teste_123",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["nome"] == "Usuario Teste"
    assert data["email"] == email
    assert "id" in data
    assert "senha" not in data
    assert "senha_hash" not in data


def test_impedir_email_duplicado(client):
    email = f"duplicado_{uuid4().hex}@example.com"

    primeiro = client.post(
        "/users",
        json={
            "nome": "Primeiro Usuario",
            "email": email,
            "senha": "senha_teste_123",
        },
    )
    assert primeiro.status_code == 201

    segundo = client.post(
        "/users",
        json={
            "nome": "Segundo Usuario",
            "email": email,
            "senha": "outra_senha_123",
        },
    )

    assert segundo.status_code == 400
    assert segundo.json()["detail"] == "E-mail já cadastrado"


def test_cadastro_com_campos_ausentes(client):
    response = client.post("/users", json={"nome": "Sem email e sem senha"})

    assert response.status_code == 422


def test_cadastro_com_email_invalido(client):
    response = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": "isso-nao-e-um-email",
            "senha": "senha_teste_123",
        },
    )

    assert response.status_code == 422


def test_cadastro_com_senha_curta(client):
    response = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": f"curta_{uuid4().hex}@example.com",
            "senha": "123",
        },
    )

    assert response.status_code == 422


def test_email_duplicado_ignora_maiusculas(client):
    email = f"maiuscula_{uuid4().hex}@example.com"

    primeiro = client.post(
        "/users",
        json={"nome": "Primeiro", "email": email, "senha": "senha_teste_123"},
    )
    assert primeiro.status_code == 201

    segundo = client.post(
        "/users",
        json={
            "nome": "Segundo",
            "email": email.upper(),
            "senha": "senha_teste_123",
        },
    )

    assert segundo.status_code == 400
    assert segundo.json()["detail"] == "E-mail já cadastrado"