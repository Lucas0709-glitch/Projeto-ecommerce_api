def test_cadastrar_produto(client, auth_headers):
    response = client.post(
        "/products",
        json={
            "nome": "Teclado",
            "descricao": "Teclado mecânico",
            "preco": 150.0,
            "estoque": 10,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["nome"] == "Teclado"
    assert data["descricao"] == "Teclado mecânico"
    assert data["preco"] == 150.0
    assert data["estoque"] == 10
    assert "id" in data


def test_listar_produtos(client, auth_headers, criar_produto):
    produto_id = criar_produto(auth_headers)

    response = client.get("/products", headers=auth_headers)

    assert response.status_code == 200

    ids = [produto["id"] for produto in response.json()]
    assert produto_id in ids


def test_consultar_produto_por_id(client, auth_headers, criar_produto):
    produto_id = criar_produto(auth_headers, nome="Mouse de Teste")

    response = client.get(f"/products/{produto_id}", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Mouse de Teste"


def test_consultar_produto_inexistente(client, auth_headers):
    response = client.get("/products/999999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_atualizar_produto(client, auth_headers, criar_produto):
    produto_id = criar_produto(auth_headers, nome="Teclado Antigo")

    response = client.put(
        f"/products/{produto_id}",
        json={
            "nome": "Teclado Atualizado",
            "descricao": "Modelo atualizado",
            "preco": 120.0,
            "estoque": 15,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Teclado Atualizado"
    assert data["descricao"] == "Modelo atualizado"
    assert data["preco"] == 120.0
    assert data["estoque"] == 15


def test_atualizar_produto_inexistente(client, auth_headers):
    response = client.put(
        "/products/999999",
        json={
            "nome": "Nada",
            "descricao": "Nada",
            "preco": 1.0,
            "estoque": 1,
        },
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_excluir_produto(client, auth_headers, criar_produto):
    produto_id = criar_produto(auth_headers)

    response = client.delete(f"/products/{produto_id}", headers=auth_headers)
    assert response.status_code in (200, 204)

    consulta = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert consulta.status_code == 404


def test_excluir_produto_inexistente(client, auth_headers):
    response = client.delete("/products/999999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_cadastrar_produto_com_preco_negativo(client, auth_headers):
    response = client.post(
        "/products",
        json={
            "nome": "Produto Inválido",
            "descricao": "Teste de preço negativo",
            "preco": -10.0,
            "estoque": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_cadastrar_produto_com_estoque_negativo(client, auth_headers):
    response = client.post(
        "/products",
        json={
            "nome": "Produto Inválido",
            "descricao": "Teste de estoque negativo",
            "preco": 10.0,
            "estoque": -1,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_cadastrar_produto_com_nome_vazio(client, auth_headers):
    response = client.post(
        "/products",
        json={
            "nome": "",
            "descricao": "Teste de nome vazio",
            "preco": 10.0,
            "estoque": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_produtos_exigem_autenticacao(client):
    corpo = {
        "nome": "Produto",
        "descricao": "Descrição",
        "preco": 10.0,
        "estoque": 1,
    }

    assert client.post("/products", json=corpo).status_code == 401
    assert client.get("/products").status_code == 401
    assert client.get("/products/1").status_code == 401
    assert client.put("/products/1", json=corpo).status_code == 401
    assert client.delete("/products/1").status_code == 401


def test_impedir_excluir_produto_que_esta_em_pedido(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers)
    pedido_id = criar_pedido(auth_headers)

    client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 1},
        headers=auth_headers,
    )

    response = client.delete(f"/products/{produto_id}", headers=auth_headers)

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Produto já foi vendido e não pode ser excluído"
    )

    consulta = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert consulta.status_code == 200