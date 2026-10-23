import pytest

from fastapi.testclient import TestClient
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.api.deps import get_db


# Banco de dados exclusivo para testes
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Criar as tabelas no banco de testes
Base.metadata.create_all(bind=engine)


# Substituir a conexão normal pela conexão de testes
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def obter_token():
    email = f"teste_{uuid4().hex}@example.com"
    senha = "TesteSenha123!"

    cadastro = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": email,
            "senha": senha,
        },
    )
    assert cadastro.status_code == 201

    resposta = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": senha,
        },
    )
    assert resposta.status_code == 200

    return resposta.json()["access_token"]


def headers_autenticacao():
    token = obter_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers():
    return headers_autenticacao()

def criar_produto(headers, preco=20.0, estoque=10):
    response = client.post(
        "/products",
        json={
            "nome": "Produto de Teste",
            "descricao": "Produto criado em teste",
            "preco": preco,
            "estoque": estoque
        },
        headers=headers
    )
    assert response.status_code == 201
    return response.json()["id"]


def criar_pedido(headers):
    response = client.post("/orders", headers=headers)
    assert response.status_code == 201
    return response.json()["id"]

def test_rota_principal():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "E-commerce API funcionando!"
    }

def test_cadastrar_usuario():
    email = f"cadastro_{uuid4().hex}@example.com"
    response = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": email,
            "senha": "senha_teste_123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Usuario Teste"
    assert data["email"] == email
    assert "id" in data
    assert "senha" not in data
    assert "senha_hash" not in data

def test_impedir_email_duplicado():
    email = f"duplicado_{uuid4().hex}@example.com"
    
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


def test_cadastrar_produto():
    response = client.post(
    "/products",
    json={
        "nome": "Teclado",
        "descricao": "Teclado mecânico",
        "preco": 150.0,
        "estoque": 10
    },
    headers=headers_autenticacao(),
    )

    assert response.status_code == 201

    data = response.json()
    assert data["nome"] == "Teclado"
    assert data["descricao"] == "Teclado mecânico"
    assert data["preco"] == 150.0
    assert data["estoque"] == 10
    assert "id" in data



def test_listar_produtos():
    email = f"teste_{uuid4().hex}@example.com"
    senha = "TesteSenha123!"

    cadastro = client.post(
        "/users",
        json={
            "nome": "Usuario Teste",
            "email": email,
            "senha": senha,
        },
    )
    assert cadastro.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": senha,
        },
    )
    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_consultar_produto_por_id(auth_headers):
    cadastro = client.post(
        "/products",
        json={
            "nome": "Mouse de Teste",
            "descricao": "Mouse para teste automatizado",
            "preco": 80.0,
            "estoque": 15
        },
        headers=auth_headers
    )

    assert cadastro.status_code == 201
    produto_id = cadastro.json()["id"]

    response = client.get(f"/products/{produto_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Mouse de Teste"


def test_excluir_produto(auth_headers):
    cadastro = client.post(
        "/products",
        json={
            "nome": "Produto para Exclusão",
            "descricao": "Produto criado para testar a exclusão",
            "preco": 25.0,
            "estoque": 5
        },
        headers=auth_headers
    )

    assert cadastro.status_code == 201
    produto_id = cadastro.json()["id"]

    response = client.delete(f"/products/{produto_id}", headers=auth_headers)

    assert response.status_code in (200, 204)

    consulta = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert consulta.status_code == 404


def test_atualizar_produto(auth_headers):
    cadastro = client.post(
        "/products",
        json={
            "nome": "Teclado Antigo",
            "descricao": "Modelo antigo",
            "preco": 100.0,
            "estoque": 10
        },
        headers=auth_headers
    )

    assert cadastro.status_code == 201
    produto_id = cadastro.json()["id"]

    response = client.put(
        f"/products/{produto_id}",
        json={
            "nome": "Teclado Atualizado",
            "descricao": "Modelo atualizado",
            "preco": 120.0,
            "estoque": 15
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Teclado Atualizado"
    assert data["descricao"] == "Modelo atualizado"
    assert data["preco"] == 120.0
    assert data["estoque"] == 15


def test_cadastrar_produto_com_dados_invalidos(auth_headers):
    response = client.post(
        "/products",
        json={
            "nome": "Produto Inválido",
            "descricao": "Teste de preço negativo",
            "preco": -10.0,
            "estoque": 5
        },
        headers=auth_headers
    )

    assert response.status_code == 422

def test_cadastrar_pedido(auth_headers):
    response = client.post("/orders", headers=auth_headers)

    assert response.status_code == 201

    data = response.json()
    assert data["status"] == "aberto"
    assert data["total"] == 0
    assert "id" in data


def test_adicionar_produto_ao_pedido(auth_headers):
    produto_id = criar_produto(auth_headers, preco=20.0, estoque=10)
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={
            "pedido_id": pedido_id,
            "produto_id": produto_id,
            "quantidade": 3
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    item = response.json()
    assert item["pedido_id"] == pedido_id
    assert item["produto_id"] == produto_id
    assert item["quantidade"] == 3
    assert item["preco_unitario"] == 20.0

    produto = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert produto.json()["estoque"] == 7

    pedido = client.get(f"/orders/{pedido_id}", headers=auth_headers)
    assert pedido.status_code == 200
    assert pedido.json()["total"] == 60.0


def test_impedir_pedido_com_estoque_insuficiente(auth_headers):
    produto_id = criar_produto(auth_headers, preco=10.0, estoque=2)
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={
            "pedido_id": pedido_id,
            "produto_id": produto_id,
            "quantidade": 3
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Estoque insuficiente"

    produto = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert produto.json()["estoque"] == 2


def test_impedir_adicionar_produto_inexistente(auth_headers):
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={
            "pedido_id": pedido_id,
            "produto_id": 999999,
            "quantidade": 1
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_impedir_adicionar_item_a_pedido_fechado(auth_headers):
    produto_id = criar_produto(auth_headers, preco=30.0, estoque=5)
    pedido_id = criar_pedido(auth_headers)

    fechamento = client.put(
        f"/orders/{pedido_id}/close", headers=auth_headers
    )
    assert fechamento.status_code == 200
    assert fechamento.json()["status"] == "fechado"

    response = client.post(
        "/orders/items",
        json={
            "pedido_id": pedido_id,
            "produto_id": produto_id,
            "quantidade": 1
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Não é possível adicionar itens a um pedido fechado"
    )

    produto = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert produto.json()["estoque"] == 5


def test_fechar_pedido_inexistente(auth_headers):
    response = client.put("/orders/999999/close", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"


def test_pedidos_exigem_autenticacao():
    assert client.post("/orders").status_code == 401
    assert client.get("/orders").status_code == 401
    assert client.get("/orders/1").status_code == 401
    assert client.get("/orders/1/items").status_code == 401
    assert client.put("/orders/1/close").status_code == 401

    resposta = client.post(
        "/orders/items",
        json={"pedido_id": 1, "produto_id": 1, "quantidade": 1}
    )
    assert resposta.status_code == 401


def test_usuario_nao_acessa_pedido_de_outro():
    headers_a = headers_autenticacao()
    headers_b = headers_autenticacao()

    produto_id = criar_produto(headers_a)
    pedido_id = criar_pedido(headers_a)

    # O usuário B tenta mexer no pedido do usuário A
    assert client.get(
        f"/orders/{pedido_id}", headers=headers_b
    ).status_code == 404

    assert client.get(
        f"/orders/{pedido_id}/items", headers=headers_b
    ).status_code == 404

    assert client.put(
        f"/orders/{pedido_id}/close", headers=headers_b
    ).status_code == 404

    resposta = client.post(
        "/orders/items",
        json={
            "pedido_id": pedido_id,
            "produto_id": produto_id,
            "quantidade": 1
        },
        headers=headers_b
    )
    assert resposta.status_code == 404

    # O dono continua enxergando o pedido normalmente
    assert client.get(
        f"/orders/{pedido_id}", headers=headers_a
    ).status_code == 200


def test_listar_meus_pedidos():
    headers_a = headers_autenticacao()
    headers_b = headers_autenticacao()

    assert client.get("/orders", headers=headers_a).json() == []

    criar_pedido(headers_a)
    criar_pedido(headers_a)

    lista_a = client.get("/orders", headers=headers_a)
    assert lista_a.status_code == 200
    assert len(lista_a.json()) == 2

    lista_b = client.get("/orders", headers=headers_b)
    assert lista_b.json() == []