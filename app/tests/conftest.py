import os

# Precisa vir ANTES de importar o app: define uma chave só para os testes
os.environ.setdefault("SECRET_KEY", "chave-secreta-apenas-para-testes")

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.db.base import Base
from app.main import app

SENHA_PADRAO = "TesteSenha123!"


@pytest.fixture
def client():
    """Cliente de teste com um banco em memória novo para cada teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def criar_usuario(client):
    """Devolve uma função que cadastra um usuário novo."""

    def _criar(nome="Usuario Teste", senha=SENHA_PADRAO):
        email = f"teste_{uuid4().hex}@example.com"
        response = client.post(
            "/users",
            json={"nome": nome, "email": email, "senha": senha},
        )
        assert response.status_code == 201
        return {"id": response.json()["id"], "email": email, "senha": senha}

    return _criar


@pytest.fixture
def fazer_login(client):
    """Devolve uma função que faz login e retorna o header de autenticação."""

    def _login(usuario):
        response = client.post(
            "/auth/login",
            data={
                "username": usuario["email"],
                "password": usuario["senha"],
            },
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _login


@pytest.fixture
def novo_usuario_logado(criar_usuario, fazer_login):
    """Devolve uma função que cria um usuário e já retorna o header dele."""

    def _novo():
        return fazer_login(criar_usuario())

    return _novo


@pytest.fixture
def auth_headers(novo_usuario_logado):
    """Header de autenticação de um usuário novo."""
    return novo_usuario_logado()


@pytest.fixture
def criar_produto(client):
    """Devolve uma função que cadastra um produto e retorna o id."""

    def _criar(headers, preco=20.0, estoque=10, nome="Produto de Teste"):
        response = client.post(
            "/products",
            json={
                "nome": nome,
                "descricao": "Produto criado em teste",
                "preco": preco,
                "estoque": estoque,
            },
            headers=headers,
        )
        assert response.status_code == 201
        return response.json()["id"]

    return _criar


@pytest.fixture
def criar_pedido(client):
    """Devolve uma função que cria um pedido e retorna o id."""

    def _criar(headers):
        response = client.post("/orders", headers=headers)
        assert response.status_code == 201
        return response.json()["id"]

    return _criar