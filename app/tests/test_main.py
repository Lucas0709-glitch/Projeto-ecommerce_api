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
            "nome": "Teclado de Teste",
            "descricao": "Teclado para teste automatizado",
            "preco": 150.0,
            "estoque": 10
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["nome"] == "Teclado de Teste"
    assert data["descricao"] == "Teclado para teste automatizado"
    assert data["preco"] == 150.0
    assert data["estoque"] == 10
    assert "id" in data


def test_listar_produtos():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_consultar_produto_por_id():
    cadastro = client.post(
        "/products",
        json={
            "nome": "Mouse de Teste",
            "descricao": "Mouse para teste automatizado",
            "preco": 80.0,
            "estoque": 15
        }
    )

    assert cadastro.status_code == 201
    produto_id = cadastro.json()["id"]

    response = client.get(f"/products/{produto_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Mouse de Teste"


def test_excluir_produto():
    cadastro = client.post(
        "/products",
        json={
            "nome": "Produto para Exclusão",
            "descricao": "Produto criado para testar a exclusão",
            "preco": 25.0,
            "estoque": 5
        }
    )

    assert cadastro.status_code == 201
    produto_id = cadastro.json()["id"]

    response = client.delete(f"/products/{produto_id}")

    assert response.status_code in (200, 204)

    consulta = client.get(f"/products/{produto_id}")
    assert consulta.status_code == 404


def test_atualizar_produto():
    cadastro = client.post(
        "/products",
        json={
            "nome": "Teclado Antigo",
            "descricao": "Modelo antigo",
            "preco": 100.0,
            "estoque": 10
        }
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
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Teclado Atualizado"
    assert data["descricao"] == "Modelo atualizado"
    assert data["preco"] == 120.0
    assert data["estoque"] == 15


def test_cadastrar_produto_com_dados_invalidos():
    response = client.post(
        "/products",
        json={
            "nome": "Produto Inválido",
            "descricao": "Teste de preço negativo",
            "preco": -10.0,
            "estoque": 5
        }
    )

    assert response.status_code == 422


def test_cadastrar_pedido():
    email = f"pedido_{uuid4().hex}@example.com"

    cadastro_usuario = client.post(
        "/users",
        json={
            "nome": "Usuario do Pedido",
            "email": email,
            "senha": "senha_teste_123"
        }
    )

    assert cadastro_usuario.status_code == 201
    usuario_id = cadastro_usuario.json()["id"]

    response = client.post(
        "/orders",
        json={"usuario_id": usuario_id}
    )

    assert response.status_code == 201

    data = response.json()
    assert data["usuario_id"] == usuario_id
    assert data["status"] == "aberto"
    assert data["total"] == 0
    assert "id" in data
