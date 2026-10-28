import pytest


def test_cadastrar_pedido(client, auth_headers):
    response = client.post("/orders", headers=auth_headers)

    assert response.status_code == 201

    data = response.json()
    assert data["status"] == "aberto"
    assert data["total"] == 0
    assert "id" in data


def test_adicionar_produto_ao_pedido(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers, preco=20.0, estoque=10)
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 3},
        headers=auth_headers,
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
    assert pedido.json()["total"] == 60.0


def test_impedir_pedido_com_estoque_insuficiente(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers, preco=10.0, estoque=2)
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 3},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Estoque insuficiente"

    produto = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert produto.json()["estoque"] == 2


def test_permitir_quantidade_igual_ao_estoque(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers, preco=10.0, estoque=3)
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 3},
        headers=auth_headers,
    )

    assert response.status_code == 201

    produto = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert produto.json()["estoque"] == 0


@pytest.mark.parametrize("quantidade", [0, -1])
def test_impedir_quantidade_invalida(
    client, auth_headers, criar_produto, criar_pedido, quantidade
):
    produto_id = criar_produto(auth_headers)
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={
            "pedido_id": pedido_id,
            "produto_id": produto_id,
            "quantidade": quantidade,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_impedir_adicionar_produto_inexistente(
    client, auth_headers, criar_pedido
):
    pedido_id = criar_pedido(auth_headers)

    response = client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": 999999, "quantidade": 1},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_impedir_adicionar_item_a_pedido_fechado(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers, preco=30.0, estoque=5)
    pedido_id = criar_pedido(auth_headers)

    fechamento = client.put(f"/orders/{pedido_id}/close", headers=auth_headers)
    assert fechamento.status_code == 200
    assert fechamento.json()["status"] == "fechado"

    response = client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 1},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Não é possível adicionar itens a um pedido fechado"
    )

    produto = client.get(f"/products/{produto_id}", headers=auth_headers)
    assert produto.json()["estoque"] == 5


def test_fechar_pedido_inexistente(client, auth_headers):
    response = client.put("/orders/999999/close", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"


def test_fechar_pedido_ja_fechado(client, auth_headers, criar_pedido):
    pedido_id = criar_pedido(auth_headers)

    primeiro = client.put(f"/orders/{pedido_id}/close", headers=auth_headers)
    assert primeiro.status_code == 200

    segundo = client.put(f"/orders/{pedido_id}/close", headers=auth_headers)

    assert segundo.status_code == 400
    assert segundo.json()["detail"] == "Pedido já está fechado"


def test_consultar_pedido_inexistente(client, auth_headers):
    response = client.get("/orders/999999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"


def test_total_do_pedido_com_varios_itens(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_a = criar_produto(auth_headers, preco=10.0, estoque=10, nome="A")
    produto_b = criar_produto(auth_headers, preco=5.5, estoque=10, nome="B")
    pedido_id = criar_pedido(auth_headers)

    for produto_id, quantidade in ((produto_a, 2), (produto_b, 3)):
        response = client.post(
            "/orders/items",
            json={
                "pedido_id": pedido_id,
                "produto_id": produto_id,
                "quantidade": quantidade,
            },
            headers=auth_headers,
        )
        assert response.status_code == 201

    pedido = client.get(f"/orders/{pedido_id}", headers=auth_headers)

    # 2 x 10.0 + 3 x 5.5 = 36.5
    assert pedido.json()["total"] == pytest.approx(36.5)


def test_listar_itens_do_pedido(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers)
    pedido_id = criar_pedido(auth_headers)

    client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 2},
        headers=auth_headers,
    )

    response = client.get(f"/orders/{pedido_id}/items", headers=auth_headers)

    assert response.status_code == 200

    itens = response.json()
    assert len(itens) == 1
    assert itens[0]["produto_id"] == produto_id
    assert itens[0]["quantidade"] == 2


def test_preco_do_item_nao_muda_quando_produto_e_atualizado(
    client, auth_headers, criar_produto, criar_pedido
):
    produto_id = criar_produto(auth_headers, preco=20.0, estoque=10)
    pedido_id = criar_pedido(auth_headers)

    client.post(
        "/orders/items",
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 2},
        headers=auth_headers,
    )

    # O preço do produto sobe depois da compra
    atualizacao = client.put(
        f"/products/{produto_id}",
        json={
            "nome": "Produto de Teste",
            "descricao": "Produto criado em teste",
            "preco": 50.0,
            "estoque": 8,
        },
        headers=auth_headers,
    )
    assert atualizacao.status_code == 200

    itens = client.get(f"/orders/{pedido_id}/items", headers=auth_headers)
    assert itens.json()[0]["preco_unitario"] == 20.0

    pedido = client.get(f"/orders/{pedido_id}", headers=auth_headers)
    assert pedido.json()["total"] == 40.0


def test_pedidos_exigem_autenticacao(client):
    assert client.post("/orders").status_code == 401
    assert client.get("/orders").status_code == 401
    assert client.get("/orders/1").status_code == 401
    assert client.get("/orders/1/items").status_code == 401
    assert client.put("/orders/1/close").status_code == 401

    resposta = client.post(
        "/orders/items",
        json={"pedido_id": 1, "produto_id": 1, "quantidade": 1},
    )
    assert resposta.status_code == 401


def test_usuario_nao_acessa_pedido_de_outro(
    client, novo_usuario_logado, criar_produto, criar_pedido
):
    headers_a = novo_usuario_logado()
    headers_b = novo_usuario_logado()

    produto_id = criar_produto(headers_a)
    pedido_id = criar_pedido(headers_a)

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
        json={"pedido_id": pedido_id, "produto_id": produto_id, "quantidade": 1},
        headers=headers_b,
    )
    assert resposta.status_code == 404

    assert client.get(
        f"/orders/{pedido_id}", headers=headers_a
    ).status_code == 200


def test_listar_meus_pedidos(client, novo_usuario_logado, criar_pedido):
    headers_a = novo_usuario_logado()
    headers_b = novo_usuario_logado()

    assert client.get("/orders", headers=headers_a).json() == []

    criar_pedido(headers_a)
    criar_pedido(headers_a)

    lista_a = client.get("/orders", headers=headers_a)
    assert lista_a.status_code == 200
    assert len(lista_a.json()) == 2

    lista_b = client.get("/orders", headers=headers_b)
    assert lista_b.json() == []