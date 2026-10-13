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